"""Internal implementation package for the Documentation Compiler."""

from .engine import CompileResult, compile_corpus, resolve_address
from .model import CompilerError

__all__ = ["CompileResult", "CompilerError", "compile_corpus", "resolve_address"]
