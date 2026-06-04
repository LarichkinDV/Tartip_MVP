\# AGENTS.md



\## Project



You are working on the BIM5D Cost-Schedule Matching project.



The project implements a local-first system for mapping BIM model elements to KSI classifier codes, calculation units, work types, GESN norm candidates, work quantities, work packages, schedule tasks, actual records, plan-fact comparisons, and control decisions.



\## Required reading before any domain or infrastructure change



Read these files first:



1\. docs/01-methodology.md

2\. docs/02-domain-model.md

3\. docs/grace/knowledge-graph.xml

4\. docs/grace/module-contracts.xml

5\. docs/grace/verification-plan.xml

6\. docs/grace/execution-packets.xml



\## Non-negotiable domain rules



1\. A BIM element is not equal to a construction work.

2\. KSI is a classification layer and must not directly select GESN.

3\. CalculationUnit is a normative-calculation template, not a universal container.

4\. ActualRecord is primarily linked to WorkPackage / zone, not to an isolated BIM element.

5\. ScheduleTask is created for WorkPackage, not for every GESN norm.

6\. Every classifier, norm, matching rule, and calculation unit must have version and status.

7\. Ambiguous matches must return `requires\_review`.

8\. Do not hard-code normative labor, cost, or GESN values as final truth without source and version fields.



\## Forbidden architecture



Do not introduce:



\- direct ModelElement -> GESNNorm mapping;

\- direct KSIResultCode -> GESNNorm selection;

\- direct GESNNorm -> ScheduleTask creation;

\- CalculationUnit storing actual fact data;

\- ActualRecord linked only to a single ModelElement;

\- hidden auto-confirmed matching when required data is incomplete.



\## Required stack



Backend:

\- Python

\- FastAPI

\- SQLAlchemy

\- Alembic

\- PostgreSQL

\- Pydantic

\- pytest



Frontend:

\- TypeScript

\- React

\- Vite



Infrastructure:

\- Docker Compose

\- Makefile

\- GitHub Actions or GitLab CI



\## Work discipline



Before implementation:

1\. Identify the execution packet.

2\. Identify affected modules.

3\. Check the knowledge graph.

4\. Check module contracts.

5\. Check verification requirements.



After implementation:

1\. Run formatting.

2\. Run linting.

3\. Run tests.

4\. Update documentation.

5\. Update CHANGELOG.md.



\## Forbidden actions



Do not:

\- delete migrations;

\- rewrite Git history;

\- commit secrets;

\- modify `.env` except `.env.example`;

\- remove GRACE artifacts;

\- add external services without documenting them;

\- bypass tests or verification scenarios.

## Reference data discipline

No source — no rule.

Codex may create:

- candidate;
- draft;
- structured question;
- review item;
- data requirement.

Codex must not create an active matching rule from memory, assumptions, or LLM-generated data.

LLM-generated content is forbidden as evidence.

Official normative fields require official evidence:

- GESN code;
- norm unit;
- included works;
- excluded works;
- resource composition;
- coefficients;
- FSNB version;
- technical part references.

Official classifier fields require official classifier evidence:

- KSI code;
- KSI name;
- KSI table;
- KSI version.

User decisions are allowed only for project entities:

- internal work types;
- work packages;
- grouping rules;
- project naming.

A user decision must not confirm normative FSNB fields or official KSI codes.

If required evidence is missing, create a structured record in `data/questions/`.

