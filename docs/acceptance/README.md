# Acceptance Reports

This directory contains packet-level acceptance reports prepared by Codex for user review.

The single acceptance overview is generated in `docs/acceptance-dashboard.md` and
`docs/acceptance-dashboard.yml`. The dashboard does not replace packet-level
reports; it only aggregates their current state.

Codex may set `ready_for_acceptance`, but must not set `accepted`, `rejected`, or `needs_revision`. The acceptance owner is the user.

User acceptance flow:

1. Open the relevant `<PACKET_ID>.acceptance.md` report.
2. Review listed artifacts and criteria.
3. Run the verification commands.
4. Fill `acceptance_decision`, `accepted_by`, `accepted_at`, and `comments` manually.

`accepted_by` must not be `Codex`.

Accepted artifacts are protected. Any material change to an accepted artifact
requires explicit user approval and repeat acceptance if the artifact changes.
