"""Own inherited .folder.json conventions for the contents of directories."""
from __future__ import annotations
import json, re
from dataclasses import dataclass
from pathlib import Path
CONFIG_NAME = ".folder.json"
SCHEMES = {"decimal", "alpha", "none", ""}
SORTS = {"alphabetical", "numerical", "date", "size", "none"}
LEGACY_SEPARATORS = (" ", ". ")
class ConventionError(ValueError): pass
@dataclass(frozen=True)
class NamespaceConvention:
    scheme: str = "decimal"; separator: str = " "; sort: str = "none"; managed: bool = False; coordinate_scheme: str | None = "decimal"
@dataclass(frozen=True)
class FolderConvention:
    folders: NamespaceConvention = NamespaceConvention(); files: NamespaceConvention = NamespaceConvention()
LEGACY_DEFAULT = FolderConvention()
def _namespace(value, inherited, owner, key):
    if value is None: return inherited
    if not isinstance(value, dict): raise ConventionError(f"{owner}: {key} must be an object")
    unknown=set(value)-{"scheme","separator","sort"}
    if unknown: raise ConventionError(f"{owner}: unknown {key} keys: {sorted(unknown)}")
    scheme=value.get("scheme",inherited.scheme); separator=value.get("separator",inherited.separator); sort=value.get("sort",inherited.sort)
    if not isinstance(scheme,str) or scheme not in SCHEMES: raise ConventionError(f"{owner}: {key}.scheme must be decimal, alpha, none, or empty")
    if not isinstance(separator,str): raise ConventionError(f"{owner}: {key}.separator must be a string")
    if not isinstance(sort,str) or sort not in SORTS: raise ConventionError(f"{owner}: {key}.sort must be alphabetical, numerical, date, size, or none")
    if scheme=="none" and any(k in value for k in ("separator","sort")): raise ConventionError(f"{owner}: {key}.scheme 'none' cannot also declare separator or sort")
    if scheme in {"decimal","alpha"} and separator=="": raise ConventionError(f"{owner}: {key}.separator cannot be empty for an emitting scheme")
    if scheme=="" and sort=="none": raise ConventionError(f"{owner}: {key}.scheme empty requires a deterministic sort")
    coordinate_scheme = scheme if scheme in {"decimal","alpha"} else inherited.coordinate_scheme
    return NamespaceConvention(scheme,separator,sort,True,coordinate_scheme)
def read_override(path, inherited):
    if not path.exists(): return inherited
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise ConventionError(f"{path}: invalid folder convention: {exc}") from exc
    if not isinstance(value,dict): raise ConventionError(f"{path}: root value must be an object")
    unknown=set(value)-{"folders","files"}
    if unknown: raise ConventionError(f"{path}: unknown keys: {sorted(unknown)}")
    return FolderConvention(_namespace(value.get("folders"),inherited.folders,path,"folders"),_namespace(value.get("files"),inherited.files,path,"files"))
def convention_for_children(corpus_root, directory):
    root=corpus_root.resolve(); target=directory.resolve()
    try: rel=target.relative_to(root)
    except ValueError as exc: raise ConventionError(f"{target} is outside corpus root {root}") from exc
    conv=read_override(root/CONFIG_NAME,LEGACY_DEFAULT); current=root
    for part in rel.parts:
        current=current/part; conv=read_override(current/CONFIG_NAME,conv)
    return conv
def alpha_value(token):
    if not re.fullmatch(r"[A-Za-z]+",token): raise ConventionError(f"invalid alpha token {token!r}")
    value=0
    for c in token.casefold(): value=value*26+(ord(c)-ord('a')+1)
    return value
def alpha_token(value):
    if value<1: raise ConventionError("alpha sequence values start at 1")
    chars=[]
    while value:
        value,r=divmod(value-1,26); chars.append(chr(ord('a')+r))
    return ''.join(reversed(chars))
def encoded_token(value,scheme):
    if scheme=="decimal": return str(value)
    if scheme=="alpha": return alpha_token(value)
    raise ConventionError(f"scheme {scheme!r} has no visible token")
def candidate_separators(conv): return tuple(dict.fromkeys(v for v in (conv.separator,*LEGACY_SEPARATORS) if v))
def split_recognized_prefix(name,conv):
    # Decimal prefixes have two historical Documentation System renderings.
    # Alpha is new: recognize only its declared separator so ordinary names
    # such as "Navigation Crawler.py" are never mistaken for prefixes.
    for sep in sorted(candidate_separators(conv),key=len,reverse=True):
        esc=re.escape(sep); m=re.match(rf"^([0-9]+){esc}",name)
        if m: return "decimal",int(m.group(1)),name[m.end():]
    if conv.separator:
        esc=re.escape(conv.separator); m=re.match(rf"^([A-Za-z]+){esc}",name)
        if m: return "alpha",alpha_value(m.group(1)),name[m.end():]
    return None,None,name
def canonical_prefix(value,conv): return encoded_token(value,conv.scheme)+conv.separator
def token_from_name(name,conv):
    if conv.scheme in {"","none"}: return None
    scheme,value,_=split_recognized_prefix(name,conv)
    return encoded_token(value,conv.scheme) if scheme==conv.scheme and value is not None else None
def token_sort_value(token): return int(token) if token.isdigit() else alpha_value(token)
