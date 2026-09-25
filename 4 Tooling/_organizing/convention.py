"""Own inherited .folder.json child naming conventions.

A .folder.json applies to the immediate contents of its containing directory.
Descendant directories inherit unspecified values until their own .folder.json
overrides them.  It never governs the basename of the directory that contains
it; that basename is governed by the convention of its parent directory.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path


CONFIG_NAME = ".folder.json"
SCHEMES = {"decimal", "alpha", "none", ""}
SORTS = {"alphabetical", "numerical", "date", "size", "none"}
KNOWN_SEPARATORS = (" ", ". ")


class ConventionError(ValueError):
    """Raised when folder organization policy is invalid or ambiguous."""


@dataclass(frozen=True)
class NamespaceConvention:
    scheme: str = "decimal"
    separator: str = " "
    sort: str = "none"


@dataclass(frozen=True)
class FolderConvention:
    folders: NamespaceConvention = NamespaceConvention()
    files: NamespaceConvention = NamespaceConvention()


LEGACY_DEFAULT = FolderConvention()


def _namespace(value: object, inherited: NamespaceConvention, owner: Path, key: str) -> NamespaceConvention:
    if value is None:
        return inherited
    if not isinstance(value, dict):
        raise ConventionError(f"{owner}: {key} must be an object")
    unknown = set(value) - {"scheme", "separator", "sort"}
    if unknown:
        raise ConventionError(f"{owner}: unknown {key} keys: {sorted(unknown)}")

    scheme = value.get("scheme", inherited.scheme)
    separator = value.get("separator", inherited.separator)
    sort = value.get("sort", inherited.sort)

    if not isinstance(scheme, str) or scheme not in SCHEMES:
        raise ConventionError(
            f"{owner}: {key}.scheme must be 'decimal', 'alpha', 'none', or an empty string"
        )
    if not isinstance(separator, str):
        raise ConventionError(f"{owner}: {key}.separator must be a string")
    if not isinstance(sort, str) or sort not in SORTS:
        raise ConventionError(
            f"{owner}: {key}.sort must be alphabetical, numerical, date, size, or none"
        )
    if scheme == "none" and ("separator" in value or "sort" in value):
        raise ConventionError(
            f"{owner}: {key}.scheme 'none' is unmanaged and cannot declare separator or sort"
        )
    return NamespaceConvention(scheme=scheme, separator=separator, sort=sort)


def read_override(path: Path, inherited: FolderConvention) -> FolderConvention:
    if not path.exists():
        return inherited
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConventionError(f"{path}: invalid folder convention: {exc}") from exc
    if not isinstance(value, dict):
        raise ConventionError(f"{path}: root value must be an object")
    unknown = set(value) - {"folders", "files"}
    if unknown:
        raise ConventionError(f"{path}: unknown keys: {sorted(unknown)}")
    return FolderConvention(
        folders=_namespace(value.get("folders"), inherited.folders, path, "folders"),
        files=_namespace(value.get("files"), inherited.files, path, "files"),
    )


def convention_for_children(corpus_root: Path, directory: Path) -> FolderConvention:
    """Return policy governing the immediate children of directory."""
    root = corpus_root.resolve()
    target = directory.resolve()
    try:
        rel = target.relative_to(root)
    except ValueError as exc:
        raise ConventionError(f"{target} is outside corpus root {root}") from exc

    convention = LEGACY_DEFAULT
    convention = read_override(root / CONFIG_NAME, convention)
    current = root
    for part in rel.parts:
        current = current / part
        convention = read_override(current / CONFIG_NAME, convention)
    return convention


def alpha_value(token: str) -> int:
    value = 0
    for char in token.casefold():
        if not ("a" <= char <= "z"):
            raise ConventionError(f"invalid alpha token {token!r}")
        value = value * 26 + (ord(char) - ord("a") + 1)
    return value


def alpha_token(value: int) -> str:
    if value < 1:
        raise ConventionError("alpha sequence values start at 1")
    chars: list[str] = []
    while value:
        value, remainder = divmod(value - 1, 26)
        chars.append(chr(ord("a") + remainder))
    return "".join(reversed(chars))


def encoded_token(value: int, scheme: str) -> str:
    if scheme == "decimal":
        return str(value)
    if scheme == "alpha":
        return alpha_token(value)
    raise ConventionError(f"scheme {scheme!r} does not encode a visible token")


def canonical_prefix(value: int, convention: NamespaceConvention) -> str:
    return encoded_token(value, convention.scheme) + convention.separator


def _candidate_separators(convention: NamespaceConvention) -> tuple[str, ...]:
    values = [convention.separator, *KNOWN_SEPARATORS]
    return tuple(dict.fromkeys(item for item in values if item))


def split_prefix(name: str, convention: NamespaceConvention) -> tuple[str | None, int | None, str]:
    """Split a recognized managed prefix from name.

    Canonical and known historical decimal/alpha forms are recognized.  A
    prefix-looking malformed name is rejected by normalization rather than
    guessed through.
    """
    separators = sorted(_candidate_separators(convention), key=len, reverse=True)
    for separator in separators:
        escaped = re.escape(separator)
        decimal = re.match(rf"^([0-9]+){escaped}", name)
        if decimal is not None:
            return "decimal", int(decimal.group(1)), name[decimal.end():]
        alpha = re.match(rf"^([A-Za-z]+){escaped}", name)
        if alpha is not None:
            token = alpha.group(1)
            return "alpha", alpha_value(token), name[alpha.end():]
    return None, None, name


def token_from_name(name: str, convention: NamespaceConvention) -> str | None:
    if convention.scheme in {"", "none"}:
        return None
    scheme, value, _ = split_prefix(name, convention)
    if scheme != convention.scheme or value is None:
        return None
    return encoded_token(value, convention.scheme)


def token_sort_value(token: str) -> int:
    return int(token) if token.isdigit() else alpha_value(token)
