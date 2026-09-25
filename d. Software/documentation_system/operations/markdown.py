"""Markdown command interfaces and discoverable operation declarations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from capabilities.frontmatter import FrontmatterError, load as load_frontmatter
from capabilities.markdown import MarkdownError, get_section, headings, renumber, sections
from capabilities.markdown_lint import MarkdownLintError, fix_file, lint_file, rule_policy
from capabilities.yaml import YamlError
from core import (
    Diagnostic, Effects, ExpectedFailure, Failure, Field, InputSchema, Operation,
    Probe, Result, Severity, Source, Verification, invoke, register,
)
from ._common import require_success

OWNER=Source("documentation_system.operations.markdown","d. Software/documentation_system/operations/markdown.py")
MARKDOWN=Source("documentation_system.capabilities.markdown","d. Software/capabilities/markdown.py")
LINT=Source("documentation_system.capabilities.markdown_lint","d. Software/capabilities/markdown_lint.py")
FRONTMATTER=Source("documentation_system.capabilities.frontmatter","d. Software/capabilities/frontmatter.py")
YAML=Source("documentation_system.capabilities.yaml","d. Software/capabilities/yaml.py")

def _chain(exc: BaseException):
    current=exc
    while current is not None:
        yield current
        current=current.__cause__

def _expected(exc: BaseException, path: Path, fallback: Source, symbol: str) -> ExpectedFailure:
    chain=list(_chain(exc))
    if any(isinstance(item,YamlError) for item in chain):
        origin=Source(YAML.module,YAML.file,"parse_mapping")
        name="YAML_ERROR"; classification="malformed"
        provenance=("frontmatter.load",)
    elif any(isinstance(item,FrontmatterError) for item in chain):
        origin=Source(FRONTMATTER.module,FRONTMATTER.file,"load")
        name="FRONTMATTER_ERROR"; classification="invalid-frontmatter"
        provenance=()
    elif any(isinstance(item,MarkdownError) for item in chain):
        origin=Source(MARKDOWN.module,MARKDOWN.file,symbol)
        name="MARKDOWN_ERROR"; classification="invalid-markdown"
        provenance=()
    elif any(isinstance(item,MarkdownLintError) for item in chain):
        origin=Source(LINT.module,LINT.file,symbol)
        name="MARKDOWN_LINT_ERROR"; classification="lint-failure"
        provenance=()
    else:
        origin=fallback
        name="READ_FAILED"; classification="unreadable"
        provenance=()
    return ExpectedFailure(Failure(
        origin=origin,name=name,classification=classification,
        subject={"path":str(path)},message=str(exc),
        details={"exception_type":type(exc).__name__},provenance=provenance,
    ))

def _body(path: Path) -> tuple[str,str]:
    try:
        source=path.read_text(encoding="utf-8")
        frontmatter=load_frontmatter(path)
    except (OSError,FrontmatterError) as exc:
        raise _expected(exc,path,OWNER,"load") from exc
    if frontmatter is None:
        return "",source
    if not source.endswith(frontmatter.body):
        raise ExpectedFailure(Failure(
            origin=FRONTMATTER,name="BODY_PRESERVATION_FAILED",
            classification="invalid-frontmatter",subject={"path":str(path)},
            message="frontmatter extraction did not preserve the Markdown body",
        ))
    return source[:len(source)-len(frontmatter.body)],frontmatter.body

def _headings(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    _,text=_body(path)
    try:
        return Result.success(headings(text))
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"headings") from exc

def _sections(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    _,text=_body(path)
    try:
        return Result.success([item.__dict__ for item in sections(text)])
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"sections") from exc

def _get_section(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    _,text=_body(path)
    try:
        return Result.success(get_section(text,str(inputs["selector"]),include_heading=not bool(inputs["no_heading"])))
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"get_section") from exc

def _canonical_diagnostics(path: Path, observed) -> tuple[Diagnostic,...]:
    result=[]
    for item in observed:
        origin=Source(LINT.module,LINT.file,"lint_file")
        result.append(Diagnostic(
            code=item.code,severity=Severity.ERROR,message=item.message,
            subject={"path":str(path),"line":item.line,"column":item.column},
            origin=origin,details={"fixable":item.fixable,"source":item.source},
        ))
    return tuple(result)

def _lint(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        observed=lint_file(path)
    except (MarkdownLintError,FrontmatterError,OSError) as exc:
        raise _expected(exc,path,LINT,"lint_file") from exc
    payload={"path":str(path),"diagnostics":[item.to_dict() for item in observed]}
    return Result.success(payload,diagnostics=_canonical_diagnostics(path,observed))

def _fix(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        observed,changed=fix_file(path)
    except (MarkdownLintError,FrontmatterError,OSError) as exc:
        raise _expected(exc,path,LINT,"fix_file") from exc
    payload={"path":str(path),"changed":changed,"diagnostics":[item.to_dict() for item in observed]}
    return Result.success(payload,diagnostics=_canonical_diagnostics(path,observed))

def _rules(inputs: Mapping[str,Any]) -> Result[Any]:
    return Result.success(rule_policy())

def _renumber(inputs: Mapping[str,Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    prefix,text=_body(path)
    try:
        rendered,mapping=renumber(text)
    except MarkdownError as exc:
        raise _expected(exc,path,MARKDOWN,"renumber") from exc
    changed=rendered!=text
    if bool(inputs["write"]) and changed:
        try:
            path.write_text(prefix+rendered,encoding="utf-8")
        except OSError as exc:
            raise _expected(exc,path,OWNER,"renumber") from exc
    return Result.success({"changed":changed,"mapping":mapping,"written":bool(inputs["write"])})

MARKDOWN_HEADINGS=register(Operation(
    id="markdown.headings",commands=(("markdown","headings"),),owner=Source(OWNER.module,OWNER.file,"headings"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_headings,
    effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="headings",fixture_input="path",fixture_content="# Title\n\n## 1. First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_SECTIONS=register(Operation(
    id="markdown.sections",commands=(("markdown","sections"),),owner=Source(OWNER.module,OWNER.file,"sections"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_sections,
    effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="sections",fixture_input="path",fixture_content="# Title\n\n## 1. First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_GET_SECTION=register(Operation(
    id="markdown.get-section",commands=(("markdown","get-section"),),owner=Source(OWNER.module,OWNER.file,"get_section"),
    input_schema=InputSchema((
        Field("path","path",example="fixture.md"),
        Field("selector","string",example="1"),
        Field("no_heading","boolean",required=False,default=False),
    )),handler=_get_section,effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="get-section",inputs={"selector":"1","no_heading":False},fixture_input="path",fixture_content="# Title\n\n## 1. First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_LINT=register(Operation(
    id="markdown.lint",commands=(("markdown","lint"),),owner=Source(OWNER.module,OWNER.file,"lint"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_lint,
    effects=Effects(filesystem="read"),verification=Verification(probes=(
        Probe(name="lint",fixture_input="path",fixture_content="# Title\n\n## First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_FIX=register(Operation(
    id="markdown.fix",commands=(("markdown","fix"),),owner=Source(OWNER.module,OWNER.file,"fix"),
    input_schema=InputSchema((Field("path","path",example="fixture.md"),)),handler=_fix,
    effects=Effects(filesystem="write"),verification=Verification(probes=(
        Probe(name="fix",fixture_input="path",fixture_content="# Title  \n\nBody.\n",fixture_suffix=".md"),
    )),
))
MARKDOWN_RULES=register(Operation(
    id="markdown.rules",commands=(("markdown","rules"),),owner=Source(OWNER.module,OWNER.file,"rules"),
    input_schema=InputSchema(),handler=_rules,effects=Effects(),
))
MARKDOWN_RENUMBER=register(Operation(
    id="markdown.renumber",commands=(("markdown","renumber"),),owner=Source(OWNER.module,OWNER.file,"renumber"),
    input_schema=InputSchema((
        Field("path","path",example="fixture.md"),
        Field("write","boolean",required=False,default=False),
    )),handler=_renumber,effects=Effects(filesystem="write"),verification=Verification(probes=(
        Probe(name="renumber-preview",inputs={"write":False},fixture_input="path",fixture_content="# Title\n\n## First\n\nBody.\n",fixture_suffix=".md"),
    )),
))
