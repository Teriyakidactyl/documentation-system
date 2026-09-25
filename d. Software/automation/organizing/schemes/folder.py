"""Plan deterministic reconciliation of inherited .folder.json conventions."""
from __future__ import annotations
import os,re
from dataclasses import dataclass
from pathlib import Path
from capabilities.folder import FolderError,Rename,validate as validate_renames
from ..convention import CONFIG_NAME,ConventionError,NamespaceConvention,canonical_prefix,convention_for_children,split_recognized_prefix
from ..model import CONTROLLED_SIDEBAND_DIRS,SUPPORTED_SUFFIXES,corpus_path,extract_metadata,ignored_directory_name
class FolderSchemeError(ValueError): pass
RESERVED_FILES={"README.md","SKILL.md",CONFIG_NAME}
@dataclass(frozen=True)
class NamingSequence:
    parent: Path; kind: str; scheme: str; separator: str; sort: str; entries: tuple[Path,...]
def _candidate_files(parent,names):
    out=[]
    for name in names:
        if name in RESERVED_FILES or name.startswith('.'): continue
        path=parent/name
        if path.is_symlink() or path.suffix.lower() not in SUPPORTED_SUFFIXES: continue
        if extract_metadata(path.resolve()) is not None: out.append(path.resolve())
    return out
def _parsed(path,conv):
    _,value,remainder=split_recognized_prefix(path.name,conv)
    if value is not None and not remainder: raise FolderSchemeError(f"{path}: prefix consumes complete basename")
    if value is None:
        if re.match(r"^[0-9]+(?:[)_-]|\\.(?=\\S))",path.name): raise FolderSchemeError(f"{path}: unrecognized prefix-like form (numeric)")
        if re.match(r"^[A-Za-z]{1,3}(?:[)_-])",path.name): raise FolderSchemeError(f"{path}: unrecognized prefix-like form (alpha)")
    return value,remainder
def _ordered(entries,conv):
    parsed=[(p,*_parsed(p,conv)[::-1]) for p in entries]
    if conv.sort=="alphabetical": return sorted(parsed,key=lambda x:(x[1].casefold(),x[0].name.casefold()))
    if conv.sort=="date": return sorted(parsed,key=lambda x:(x[0].stat().st_mtime_ns,x[1].casefold()))
    if conv.sort=="size": return sorted(parsed,key=lambda x:(x[0].stat().st_size,x[1].casefold()))
    if conv.sort=="numerical":
        keyed=[]
        for item in parsed:
            m=re.match(r"^([0-9]+)",item[1])
            if not m: raise FolderSchemeError(f"{item[0]}: numerical sort requires basename to begin with a number")
            keyed.append((int(m.group(1)),item))
        return [item for _,item in sorted(keyed,key=lambda p:(p[0],p[1][1].casefold()))]
    if conv.sort=="none":
        missing=[x[0].name for x in parsed if x[2] is None]
        if missing: raise FolderSchemeError(f"sticky sort requires existing recognized positions; missing on {missing}")
        vals=[x[2] for x in parsed]
        if len(vals)!=len(set(vals)): raise FolderSchemeError("sticky sort has duplicate sibling positions")
        return sorted(parsed,key=lambda x:(x[2],x[1].casefold()))
    raise FolderSchemeError(f"unsupported sort {conv.sort!r}")
def _namespace_plan(entries,conv):
    if not conv.managed or conv.scheme=="none" or not entries: return []
    if conv.scheme=="":
        out=[]
        for p in entries:
            _,value,remainder=split_recognized_prefix(p.name,conv)
            if value is None: _parsed(p,conv); continue
            out.append(Rename(p,p.with_name(remainder)))
        return out
    out=[]
    for pos,(p,remainder,_) in enumerate(_ordered(entries,conv),1):
        dst=p.with_name(canonical_prefix(pos,conv)+remainder)
        if dst.name!=p.name: out.append(Rename(p,dst))
    return out
def inspect(corpus_root):
    root=corpus_root.resolve(); seq=[]; plan=[]
    try:
        for current,dirs,files in os.walk(root,followlinks=False):
            parent=Path(current).resolve()
            dirs[:]=[n for n in dirs if n not in CONTROLLED_SIDEBAND_DIRS and not ignored_directory_name(n) and not (parent/n).is_symlink()]
            conv=convention_for_children(root,parent)
            for kind,entries,ns in (("folders",[(parent/n).resolve() for n in dirs],conv.folders),("files",_candidate_files(parent,files),conv.files)):
                seq.append(NamingSequence(parent,kind,ns.scheme,ns.separator,ns.sort,tuple(entries))); plan.extend(_namespace_plan(entries,ns))
    except (ConventionError,FolderError) as exc: raise FolderSchemeError(str(exc)) from exc
    plan.sort(key=lambda x:(-len(x.source.parent.relative_to(root).parts),corpus_path(root,x.source).casefold()))
    try: validate_renames(plan)
    except FolderError as exc: raise FolderSchemeError(str(exc)) from exc
    return seq,plan
def plan_normalization(corpus_root): return inspect(corpus_root)[1]
def as_dict(corpus_root):
    root=corpus_root.resolve(); seq,plan=inspect(root)
    return {"scheme":"folder-conventions","sequences":[{"parent":"." if x.parent==root else corpus_path(root,x.parent),"kind":x.kind,"prefix_scheme":x.scheme,"separator":x.separator,"sort":x.sort,"entries":[p.name for p in x.entries]} for x in seq],"normalization":[{"from":corpus_path(root,x.source),"to":corpus_path(root,x.destination)} for x in plan]}
