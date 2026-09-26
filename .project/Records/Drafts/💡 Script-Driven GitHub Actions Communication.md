# 💡 Script-Driven GitHub Actions Communication

## Idea

Keep workflow semantics in repository scripts while using GitHub Actions as the
presentation and orchestration layer.

GitHub Actions must declare the job graph in workflow YAML. A running script
cannot dynamically create arbitrary new job nodes after the workflow has
started. Scripts can, however, determine what happened inside those declared
jobs and communicate that state back to GitHub.

The desired division is:

~~~text
GitHub workflow YAML
    owns:
    - jobs
    - needs/dependencies
    - runners
    - matrix expansion
    - visible workflow graph

Repository scripts
    own:
    - inspection semantics
    - migration/preflight semantics
    - refresh semantics
    - idempotence semantics
    - detailed progress
    - diagnostics
    - summaries
    - machine-readable outputs
~~~

This keeps local execution and CI behavior aligned: GitHub does not become the
authority for what Organizing means merely because it visualizes the process.

## Candidate workflow shape

Expose major semantic phases as separate jobs so the Actions graph communicates
the operation at a glance:

~~~text
tests
  ↓
organization-inspection
  ↓
staged-validation
  ↓
refresh
  ↓
idempotence
~~~

For a push to `main`, an additional mutation job may follow validation:

~~~text
tests
  ↓
organization-inspection
  ↓
staged-validation
  ↓
refresh-main
  ↓
idempotence
~~~

Do not split every shell command into a job. Jobs should correspond to
maintainer-significant semantic phases because each job has runner overhead.

## Script communication

Repository scripts should remain usable outside GitHub Actions and emit ordinary
terminal output by default.

When `GITHUB_ACTIONS=true`, they can additionally use GitHub's runtime
communication surfaces:

- `$GITHUB_STEP_SUMMARY` for human-readable Markdown summaries;
- `$GITHUB_OUTPUT` for machine-readable outputs consumed by later jobs;
- workflow annotations such as `::notice`, `::warning`, and `::error`;
- log groups for expandable phase details.

For example, an Organizing inspection could summarize:

~~~text
Folder convention inspection

Folders scanned:        37
Managed namespaces:     52
Planned renames:        73
Literal path rewrites:  57
Ambiguous references:    0
Diagnostics:             0

Convention migration is safe to apply.
~~~

A canonical no-op state could report:

~~~text
Organization state

Planned renames:         0
Path rewrites:           0
Diagnostics:             0

Repository is already canonical.
~~~

## Job outputs

Scripts can expose facts that predefined jobs use to decide whether to run.

For example, inspection might publish:

~~~text
renames=73
literal_rewrites=57
safe=true
~~~

A predefined migration job could then be conditional on whether work exists.
Skipped nodes remain visible in the graph, which can communicate useful state
such as "migration skipped — repository already canonical."

This is dynamic execution within a statically declared graph, not dynamic graph
construction.

## Tooling direction

`Navigation Crawler.py` could expose concise commands around the existing
Organizing behavior, for example:

~~~text
inspect
preflight
refresh
verify-idempotence
~~~

The same commands should drive both local work and GitHub Actions.

A concise output mode may be useful in addition to the existing detailed JSON,
for example:

~~~text
folder-conventions
directories: 37
renames: 73
literal-rewrites: 57
ambiguous-references: 0
safe: yes
~~~

GitHub Actions can project that information into job summaries without
reimplementing Organizing semantics in YAML.

## Principle

**The script knows what happened; the workflow decides where GitHub displays
it.**

The workflow should therefore be a thin orchestration and visualization shell
around repository-owned executable semantics.
