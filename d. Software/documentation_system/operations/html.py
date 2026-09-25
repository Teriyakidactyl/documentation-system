"""HTML command interfaces and discoverable operation declarations."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any, Mapping
from capabilities.html import HtmlError, anchors, inspect
from core import Effects, ExpectedFailure, Failure, Field, InputSchema, Operation, Probe, Result, Source, Verification, invoke, register

OWNER=Source("documentation_system.operations.html","d. Software/documentation_system/operations/html.py")
CAPABILITY=Source("documentation_system.capabilities.html","d. Software/capabilities/html.py")

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ExpectedFailure(Failure(
            origin=OWNER,name="READ_FAILED",classification="unreadable",
            subject={"path":str(path)},message=str(exc),
            details={"exception_type":type(exc).__name__},
        )) from exc

def _inspect(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        return Result.success([item.__dict__ for item in inspect(_read(path))])
    except HtmlError as exc:
        raise ExpectedFailure(Failure(
            origin=Source(CAPABILITY.module,CAPABILITY.file,"inspect"),
            name="HTML_ERROR",classification="malformed",subject={"path":str(path)},
            message=str(exc),details={"exception_type":type(exc).__name__},
        )) from exc

def _anchors(inputs: Mapping[str, Any]) -> Result[Any]:
    path=Path(str(inputs["path"]))
    try:
        payload=[{"start":item.start,"end":item.end,"attributes":dict(item.attributes),"text":item.text} for item in anchors(_read(path))]
        return Result.success(payload)
    except HtmlError as exc:
        raise ExpectedFailure(Failure(
            origin=Source(CAPABILITY.module,CAPABILITY.file,"anchors"),
            name="HTML_ERROR",classification="malformed",subject={"path":str(path)},
            message=str(exc),details={"exception_type":type(exc).__name__},
        )) from exc

HTML_INSPECT=register(Operation(
    id="html.inspect",commands=(("html","inspect"),),owner=Source(OWNER.module,OWNER.file,"inspect"),
    input_schema=InputSchema((Field("path","path",example="fixture.html"),)),
    handler=_inspect,effects=Effects(filesystem="read"),
    verification=Verification(probes=(Probe(name="inspect-html",fixture_input="path",fixture_content="<p>Hello</p>\n",fixture_suffix=".html"),)),
))
HTML_ANCHORS=register(Operation(
    id="html.anchors",commands=(("html","anchors"),),owner=Source(OWNER.module,OWNER.file,"anchors"),
    input_schema=InputSchema((Field("path","path",example="fixture.html"),)),
    handler=_anchors,effects=Effects(filesystem="read"),
    verification=Verification(probes=(Probe(name="inspect-anchor",fixture_input="path",fixture_content="<a uid='ABC123' href='x'>Label</a>\n",fixture_suffix=".html"),)),
))
