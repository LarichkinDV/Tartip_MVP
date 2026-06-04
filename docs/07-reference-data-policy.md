# Reference Data Policy

## 1. No Source — No Rule

`No source — no rule` is a hard project rule. Matching rules, classifier links, normative candidates, norm units, included works, excluded works, resource composition, coefficients, FSNB versions, and technical part references cannot become active without explicit trusted evidence.

Codex may create drafts, candidates, structured questions, review items, and data requirements. Codex must not invent official KSI codes, GESN codes, normative values, norm units, works composition, resources, coefficients, or technical part references.

## 2. Official Evidence And Project Decision

Official evidence is a trusted source record from `data/reference/raw/` and `data/reference/normalized/`, registered in `data/reference/manifests/source-manifest.yml` with checksum, source origin, source authority, version, and status.

Project decisions are user decisions for project-only entities: internal work types, work packages, grouping rules, project naming, and other non-normative conventions.

Project decisions are useful for local organization, but they are not official classifier or normative evidence.

## 3. Why User Confirmation Cannot Confirm Normative Fields

Normative fields are governed by official source documents and versions. User confirmation can state project intent, but it cannot transform an unofficial value, memory-based answer, or LLM-generated text into official evidence.

For FSNB/GESN and official KSI fields, the system requires official evidence from a registered source. If evidence is absent, the matching rule must remain `draft_requires_data`, `requires_review`, `requires_norm_review`, or `requires_technical_part_review`.

## 4. Reference Data Lifecycle

Reference data moves through the following layers:

- `inbox`: user places an original local source file here.
- `quarantine`: a file has been discovered but is not accepted as a trusted source.
- `raw`: immutable accepted copy with checksum and manifest metadata.
- `staging`: parsed temporary records.
- `normalized`: normalized lookup-ready records.
- `reports`: validation, import, and comparison reports.

Files in `inbox` are not trusted by default. A source becomes usable evidence only after it is accepted into `raw`, receives checksum metadata, and is represented in the manifest with an allowed authority.

## 5. Source Manifest Requirements

`data/reference/manifests/source-manifest.yml` records each accepted or candidate source. It supports the fields listed in the manifest template, including source identity, authority, origin, file paths, checksum, acquisition metadata, declared and detected versions, parser metadata, import counts, status, and notes.

Allowed `source_origin` values include official machine-readable data, official PDFs, official web pages, official manual transcription, licensed software export, project dictionary, user decision, secondary source, and LLM-generated content.

If `source_origin = llm_generated`, `source_authority` must be `forbidden`. LLM-generated content cannot be evidence.

## 6. Evidence Requirements For Matching Rules

Matching rules must include evidence slots for:

- `ksi_result_code`
- `ksi_process_code`
- `work_type`
- `gesn_norm`
- `norm_unit`
- `included_works`
- `excluded_works`
- `resource_composition`
- `technical_part_reference`

Each evidence slot should reference `source_id` and `normalized_record_id` when evidence exists. Full normative source content must not be copied into the matching rule YAML.

## 7. Delta-Based Reference Versioning

Reference releases are versioned as logical objects and object revisions. A stable `natural_key` identifies the logical reference object. A canonical `payload_jsonb` hash identifies whether the record content changed.

Unchanged records across releases reuse the previous revision. Changed records create a new revision and a change set entry. Deleted records create a delete operation. Added records create a new object and first revision.

Matching rules store dependencies on reference objects and revisions. If a depended normative object changes, the rule must be marked for normative review, such as `requires_norm_review`.

## 8. When To Create Questions

Create a `data requirement` when a required source file, official source, version, or export is missing.

Create a `mapping question` when project entities cannot be mapped confidently because required context is ambiguous.

Create a `normative review question` when GESN applicability, technical parts, norm units, works composition, resources, coefficients, or source versioning require expert review.

Create a `project decision` when the user must choose project-only naming, grouping, work package, or internal work type behavior.

Create an `import issue` when a local source file exists but cannot be parsed, validated, checksummed, accepted, or normalized.

## 9. Matching Rule Statuses

- `draft_requires_data`: rule draft exists, but required source evidence is missing.
- `candidate_from_reference`: evidence exists, but the rule is still a candidate.
- `requires_review`: matching is ambiguous or incomplete.
- `requires_norm_review`: normative evidence or applicability requires review.
- `requires_technical_part_review`: technical part evidence or applicability requires review.
- `user_reviewed`: project-only decision has been reviewed by the user.
- `active`: rule is approved with all required evidence and review gates satisfied.
- `deprecated`: rule is superseded by a newer source, rule, or policy.
- `blocked`: rule cannot progress until a blocker is resolved.
