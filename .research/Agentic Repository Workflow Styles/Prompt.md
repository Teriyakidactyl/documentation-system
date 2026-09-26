---
uid: HJ78QV
form:
  path: '<a href="../../a.%20Document%20Design/a.%20Assemblies/b.%20Forms/e.%20Research/a.%20Research%20Prompt/README.md" uid="BSJY2D">documentation-system:§a.a.b.e.a</a>'
  version: '1.0'
description: >-
  `Read in full and follow when` *the agentic repository-workflow
  investigation is rerun* `to` **evaluate how a tool-using agent should
  orient, retrieve, search, and establish completeness when inspecting
  unfamiliar repositories under different harness capabilities**.
---

# Research Prompt: Agentic Repository Workflow Styles

> [!WARNING]
> **Post-documentation reconstruction.** This reusable prompt was composed
> after the interactive investigation preserved in the sibling research
> record. It reconstructs the thrust of the questions that drove that
> conversation. It was not frozen before that conversation began and must not
> be treated as the literal prompt that produced the earlier findings.

The fenced block below is the rerunnable research payload. Repository
frontmatter, the title, and the provenance warning above are not part of the
prompt.

````text
Investigate how a capable tool-using LLM agent naturally and deliberately
approaches an unfamiliar software repository when asked to compare the
coherence or design quality of one code area with another.

Use a concrete comparison such as the `Skills/` code in
`Teriyakidactyl/saps` and the `4 Tooling/` code in
`Teriyakidactyl/documentation-system` when a concrete substrate helps expose
workflow choices, but keep the primary subject the agentic workflow rather
than the verdict about those repositories.

The investigation should answer these questions:

1. Starting only from a repository URL and a comparative code-review task,
   which tools or operations should an agent call first, and in what order?
2. Where do repository-root and target-local entry documents such as
   `README.md`, `AGENTS.md`, `SKILL.md`, or harness-specific instruction
   files belong in that sequence?
3. When should the agent enumerate a directory or recursive tree, retrieve
   whole source files, search or grep across the corpus, inspect tests, or
   inspect history?
4. What information is lost when search snippets are used before the agent
   understands the repository's declared conceptual boundaries?
5. When is a whole file the appropriate reasoning unit, and when should a
   large file be read in bounded chunks?
6. How can the agent establish that a chunked read reached EOF? Distinguish
   source completeness, connector retrieval completeness, harness delivery
   completeness, and the model actually observing terminal content.
7. What stronger evidence would an artifact-native EOF marker such as
   `eof:<uid>` add, and what would it still fail to prove?
8. How does a persistent local checkout with shell access differ from a
   connector-based harness exposing typed repository operations?
9. How do those environments change the information economics of broad
   reconnaissance, filtering, aggregation, and context consumption?
10. Can a harness retrieve broadly while exposing only a compact derived view
    to the model? Distinguish retrieval breadth from context breadth.
11. What failure modes arise when an agent dumps a large recursive tree or
    grep result directly into model context instead of filtering it first?
12. Which workflow steps are best modeled as:
    - direct retrieval of a whole reasoning unit;
    - programmatic reconnaissance over broad metadata;
    - targeted cross-corpus search used to test an architectural hypothesis?
13. What do these observations imply for documentation systems designed for
    amnesiac agents and for repository information architecture more broadly?

When evaluating the workflow, distinguish at least:

- orientation: acquiring enough repository-local state to interpret the target;
- topology discovery: learning what units and relationships exist;
- unit understanding: reading complete files or bounded units in context;
- hypothesis testing: searching the corpus for dependency or ownership
  violations;
- completion evidence: establishing that required retrieval reached its
  intended boundary;
- context management: deciding what retrieved information should actually
  enter the model's working context.

Compare a connector-based workflow with a local-shell workflow without
assuming that either is universally superior. Account for the specific
capabilities of the harness. A connector may offer structured operations and
orchestration that can retrieve or process broad external state without
placing every raw result into model context. A local checkout may permit cheap
arbitrary filesystem analysis and custom scripts before any output is shown to
the model.

For any concrete tool sequence, explain why each operation appears where it
does. In particular, test whether recursive enumeration should precede or
follow local README or other entry guidance, and whether grep/search should be
an orientation mechanism or a later hypothesis-testing mechanism.

Record any live workflow failures that reveal the model, connector, or harness
boundary, such as a tool response that is complete at the API layer but
truncated before the model can consume all of it.

The output should contain:

1. a default repository-inspection sequence;
2. a description of exceptions that change that sequence;
3. a comparison of whole-file reading, tree reconnaissance, and grep/search;
4. a model of EOF and truncation evidence across source, connector, harness,
   and model-observation layers;
5. a comparison of persistent local checkout and structured connector
   environments;
6. an explanation of retrieval breadth versus context breadth;
7. concrete implications for designing agent-facing repository workflows and
   documentation surfaces;
8. limitations separating observed harness behavior from proposed design
   improvements.

Do not infer that a tool call's success proves that the model observed the
entire returned representation. Do not infer repository architecture from
search snippets alone when entry guidance or whole-unit structure is available.
````
