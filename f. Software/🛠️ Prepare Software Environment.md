---
uid: THAV5S
description: >-
  `Read in full and follow when` *Documentation System Python tooling cannot
  import a required package, pip is unavailable, or the host Python is
  externally managed* `to` **create a repository-local virtual environment,
  install the declared Software dependencies, and run Documentation System tools
  without modifying system Python**.
quadrant: HowTo
outline:
  topology: linear
  numbering: hierarchical-decimal
writing-style:
  formality: professional
  tone: neutral/detached
  mode: imperative
  density: moderate
  abstraction: concrete/specific
  redundancy: zero
  signposting: light
  register: technical
---

# 🛠️ Prepare Software Environment

Use one repository-local Python environment for Documentation System Software.
Do not install Software libraries into the operating system's Python
installation.

## 1. Confirm host prerequisites

Confirm `python3` is available and can create virtual environments:

```bash
python3 --version
python3 -m venv --help
```

When the `venv` module is unavailable, install the host package that supplies
it before continuing. On Debian 13, the package is `python3-venv`:

```bash
sudo apt-get update
sudo apt-get install -y python3-venv
```

Administrator authorization is required for the package-manager step. If it is
not available, use an already provisioned Python environment instead of
modifying the system interpreter.

## 2. Create the repository environment

Create the environment at the repository root:

```bash
python3 -m venv .venv-docs
```

Reuse an existing `.venv-docs` when its interpreter is healthy. The
environment is repository working state, not controlled documentation.

## 3. Install Software dependencies

Set `TOOLING` to the installed Documentation System Software directory. For a
consumer repository whose Documentation System is installed beneath
`docs/1 Documentation System`:

```bash
TOOLING="docs/1 Documentation System/f. Software"
.venv-docs/bin/python -m pip install -r "$TOOLING/requirements.txt"
```

In this repository, use `TOOLING="f. Software"`.

Install from `requirements.txt` rather than copying package names into local
setup instructions. The file is the shared dependency declaration used by
Documentation System automation and local Software environments.

Do not use `pip install --user` or `--break-system-packages` to work around
an externally managed system Python. Software imports these libraries inside its
own Python process, so a `pipx` application environment is not a substitute
for the interpreter that runs the Software modules.

## 4. Run Software through the environment

Use the environment interpreter for Documentation System Python tools and keep
the Software directory on `PYTHONPATH` when the installation is nested:

```bash
PYTHONPATH="$TOOLING" \
.venv-docs/bin/python \
"$TOOLING/Markdown.py" \
lint \
"path/to/document.md"
```

Use the same interpreter for Organizing, Frontmatter, YAML, HTML, and other
Python Software commands that share the environment.

## 5. Keep the environment local

Add `.venv-docs/` to the consuming repository's ignore rules. Do not commit
the environment or copy its installed packages into the Documentation System.

When `requirements.txt` changes, rerun its install command in the existing
environment. Recreate `.venv-docs` only when the environment itself is
damaged, its Python version is no longer suitable, or a clean rebuild is
required.
