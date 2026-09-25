"""Small runtime input contracts shared by invocation and verification."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

_MISSING = object()

class SchemaError(ValueError):
    pass

@dataclass(frozen=True)
class Field:
    name: str
    kind: str
    required: bool = True
    default: Any = _MISSING
    enum: tuple[Any, ...] = ()
    example: Any = _MISSING

    def sample(self) -> Any:
        if self.example is not _MISSING:
            return self.example
        if self.default is not _MISSING:
            return self.default
        return {"string":"example","path":"example.txt","boolean":False,"integer":1,"array":[],"object":{}}.get(self.kind, _MISSING)

    def accepts(self, value: Any) -> bool:
        if self.kind in {"string", "path"}:
            valid = isinstance(value, str)
        elif self.kind == "boolean":
            valid = isinstance(value, bool)
        elif self.kind == "integer":
            valid = isinstance(value, int) and not isinstance(value, bool)
        elif self.kind == "array":
            valid = isinstance(value, list)
        elif self.kind == "object":
            valid = isinstance(value, dict)
        else:
            raise SchemaError(f"Unsupported field kind {self.kind!r}")
        return valid and (not self.enum or value in self.enum)

@dataclass(frozen=True)
class InputSchema:
    fields: tuple[Field, ...] = ()

    def validate(self, values: Mapping[str, Any]) -> dict[str, Any]:
        by_name = {field.name: field for field in self.fields}
        unknown = sorted(set(values) - set(by_name))
        if unknown:
            raise SchemaError(f"Unknown input: {', '.join(unknown)}")
        normalized: dict[str, Any] = {}
        for field in self.fields:
            if field.name not in values:
                if field.default is not _MISSING:
                    normalized[field.name] = field.default
                    continue
                if field.required:
                    raise SchemaError(f"Missing required input: {field.name}")
                continue
            value = values[field.name]
            if not field.accepts(value):
                expected = field.kind + (f" in {list(field.enum)!r}" if field.enum else "")
                raise SchemaError(f"Invalid input {field.name}: expected {expected}")
            normalized[field.name] = value
        return normalized

    def example(self) -> dict[str, Any] | None:
        result: dict[str, Any] = {}
        for field in self.fields:
            sample = field.sample()
            if sample is _MISSING:
                if field.required:
                    return None
                continue
            result[field.name] = sample
        return result

    def invalid_examples(self) -> list[tuple[str, dict[str, Any]]]:
        seed = self.example()
        if seed is None:
            return []
        cases: list[tuple[str, dict[str, Any]]] = []
        required = [field for field in self.fields if field.required]
        if required:
            field = required[0]
            missing = dict(seed); missing.pop(field.name, None)
            cases.append((f"missing-{field.name}", missing))
        if self.fields:
            field = self.fields[0]
            wrong = dict(seed)
            wrong[field.name] = 7 if field.kind in {"string", "path"} else "wrong"
            cases.append((f"wrong-type-{field.name}", wrong))
        enum_field = next((field for field in self.fields if field.enum), None)
        if enum_field is not None:
            invalid = dict(seed); invalid[enum_field.name] = "__invalid_enum_member__"
            cases.append((f"invalid-enum-{enum_field.name}", invalid))
        return cases
