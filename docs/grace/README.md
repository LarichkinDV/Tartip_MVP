# GRACE Artifacts

This directory stores lightweight project governance artifacts used before
changing domain logic or infrastructure.

- `knowledge-graph.xml`: domain entities, allowed edges, and forbidden direct edges.
- `module-contracts.xml`: module responsibilities, inputs, outputs, and invariants.
- `verification-plan.xml`: verification scenarios for governance and versioning rules.
- `execution-packets.xml`: planned execution packets such as `EP-001-INFRA`,
  `EP-002-REFERENCE-GOVERNANCE`, and `EP-003-REFERENCE-VERSIONING`.

For `EP-001-INFRA`, Docker-dependent checks are allowed to be skipped locally when
Docker is unavailable, but the skip must be explicit. Non-Docker checks still run
through `make format`, `make lint`, `make test`, `make check`, and the reference
validation commands where applicable.
