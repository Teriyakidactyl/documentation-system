"""Plan and apply deterministic organization refactors with path-reference migration."""
from __future__ import annotations
import os,re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote
from _capabilities.folder import FolderError,Rename,apply as apply_renames
from _capabilities.html import anchors
from .model import OrganizingError,corpus_path
from .schemes.folder import FolderSchemeError,as_dict as folder_as_dict,plan_normalization as folder_plan_normalization
from .schemes.ordinal import OrdinalSchemeError,as_dict as ordinal_as_dict,plan_normalization as ordinal_plan_normalization
@dataclass(frozen=True)
class UnmanagedReference: path: Path; line: int; value: str
@dataclass(frozen=True)
class TextRewrite: path: Path; before: str; after: str; count: int
def _text_files(root):
    for current,dirs,files in os.walk(root,followlinks=False):
        parent=Path(current); dirs[:]=[n for n in dirs if (not n.startswith('.') or n=='.github') and n!='.git' and not (parent/n).is_symlink()]
        for name in files:
            p=parent/name
            if p.is_symlink(): continue
            try:
                if p.stat().st_size>2_000_000: continue
                p.read_text(encoding='utf-8')
            except (OSError,UnicodeDecodeError): continue
            yield p.resolve()
def _mask_owned_references(text):
    chars=list(text)
    for a in anchors(text):
        if a.attribute('uid') is not None:
            for i in range(a.start,a.end):
                if chars[i]!='\n': chars[i]=' '
    for m in re.finditer(r'<!--.*?-->',text,flags=re.DOTALL):
        if not re.search(r'(?m)^\s*element\s*:',m.group(0)): continue
        for i in range(m.start(),m.end()):
            if chars[i]!='\n': chars[i]=' '
    return ''.join(chars)
def _final_relative(root,relative,plan):
    value=relative; ordered=sorted(plan,key=lambda x:len(corpus_path(root,x.source)),reverse=True)
    for _ in range(len(ordered)+1):
        changed=False
        for item in ordered:
            src=corpus_path(root,item.source); dst=corpus_path(root,item.destination)
            if value==src or value.startswith(src+'/'):
                new=dst+value[len(src):]
                if new!=value: value=new; changed=True
        if not changed:return value
    raise OrganizingError(f'path migration did not converge for {relative!r}')
def _replacement_map(root,plan):
    out={}
    for item in plan:
        src=corpus_path(root,item.source); dst=_final_relative(root,src,plan); out[src]=dst; out[quote(src,safe='/@')]=quote(dst,safe='/@')
    return out
def _safe_boundary(text,start,end):
    before=text[start-1] if start else ''; after=text[end] if end<len(text) else ''
    token=lambda c:bool(c) and (c.isalnum() or c in '_.-')
    return not token(before) and not token(after)
def plan_text_rewrites(corpus_root,plan):
    root=corpus_root.resolve(); repl=_replacement_map(root,plan); patterns=sorted(repl,key=len,reverse=True); rewrites=[]; ambiguous=[]
    for path in sorted(_text_files(root),key=lambda p:corpus_path(root,p).casefold()):
        before=path.read_text(encoding='utf-8'); masked=_mask_owned_references(before); spans=[]
        for pat in patterns:
            cursor=0
            while True:
                pos=masked.find(pat,cursor)
                if pos<0:break
                end=pos+len(pat); cursor=end
                if any(pos<b and end>a for a,b,_ in spans):continue
                if not _safe_boundary(masked,pos,end): ambiguous.append(UnmanagedReference(path,masked.count('\n',0,pos)+1,pat)); continue
                spans.append((pos,end,repl[pat]))
        if spans:
            after=before
            for a,b,r in sorted(spans,reverse=True):after=after[:a]+r+after[b:]
            if after!=before:rewrites.append(TextRewrite(path,before,after,len(spans)))
    return rewrites,ambiguous
def unmanaged_references(corpus_root,plan):return plan_text_rewrites(corpus_root,plan)[1]
def uses_folder_conventions(corpus_root):return any(p.name=='.folder.json' for p in corpus_root.resolve().rglob('.folder.json'))
def _organization_payload_and_plan(corpus_root):
    try:
        if uses_folder_conventions(corpus_root):return folder_as_dict(corpus_root),folder_plan_normalization(corpus_root)
        return ordinal_as_dict(corpus_root),ordinal_plan_normalization(corpus_root)
    except (FolderSchemeError,OrdinalSchemeError) as exc:raise OrganizingError(str(exc)) from exc
def inspect_organization(corpus_root):
    root=corpus_root.resolve(); payload,plan=_organization_payload_and_plan(root); rewrites,refs=plan_text_rewrites(root,plan); payload['literal_rewrites']=[{'path':corpus_path(root,x.path),'replacements':x.count} for x in rewrites]; payload['unmanaged_references']=[{'path':corpus_path(root,x.path),'line':x.line,'value':x.value} for x in refs]; return payload
def _apply_text_rewrites(rewrites):
    written=[]
    try:
        for x in rewrites:x.path.write_text(x.after,encoding='utf-8');written.append(x)
    except OSError as exc:
        for x in reversed(written):
            try:x.path.write_text(x.before,encoding='utf-8')
            except OSError:pass
        raise OrganizingError(f'literal path migration failed before rename: {exc}') from exc
    return written
def normalize_conventions(corpus_root,*,apply=False):
    root=corpus_root.resolve(); payload,plan=_organization_payload_and_plan(root); rewrites,refs=plan_text_rewrites(root,plan); payload['literal_rewrites']=[{'path':corpus_path(root,x.path),'replacements':x.count} for x in rewrites];payload['unmanaged_references']=[{'path':corpus_path(root,x.path),'line':x.line,'value':x.value} for x in refs];payload['applied']=False
    if not apply or not plan:return payload
    if refs:raise OrganizingError('folder convention normalization has ambiguous literal path references; '+'; '.join(f"{corpus_path(root,x.path)}:{x.line} -> {x.value}" for x in refs[:8]))
    written=_apply_text_rewrites(rewrites)
    try:apply_renames(plan)
    except FolderError as exc:
        for x in reversed(written):
            try:x.path.write_text(x.before,encoding='utf-8')
            except OSError:pass
        raise OrganizingError(str(exc)) from exc
    payload['applied']=True;return payload
def normalize_ordinals(corpus_root,*,apply=False):
    root=corpus_root.resolve()
    try:payload=ordinal_as_dict(root);plan=ordinal_plan_normalization(root)
    except OrdinalSchemeError as exc:raise OrganizingError(str(exc)) from exc
    rewrites,refs=plan_text_rewrites(root,plan)
    legacy_refs=[UnmanagedReference(x.path,0,corpus_path(root,x.path)) for x in rewrites]+refs
    payload['unmanaged_references']=[{'path':corpus_path(root,x.path),'line':x.line,'value':x.value} for x in legacy_refs];payload['applied']=False
    if not apply or not plan:return payload
    if legacy_refs:raise OrganizingError('ordinal normalization is blocked by unmanaged literal path references')
    try:apply_renames(plan)
    except FolderError as exc:raise OrganizingError(str(exc)) from exc
    payload['applied']=True;return payload
