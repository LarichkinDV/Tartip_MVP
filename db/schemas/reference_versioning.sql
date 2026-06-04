-- Conceptual schema for EP-003-REFERENCE-VERSIONING.
-- This is implementation-ready DDL documentation, not an applied migration.

CREATE TABLE reference_release (
    release_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    version_label TEXT NOT NULL,
    valid_from DATE,
    valid_to DATE,
    published_at TIMESTAMPTZ,
    acquired_at TIMESTAMPTZ,
    checksum_sha256 TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE reference_object (
    object_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    object_type TEXT NOT NULL,
    natural_key TEXT NOT NULL,
    created_in_release_id TEXT NOT NULL REFERENCES reference_release(release_id),
    status TEXT NOT NULL,
    UNIQUE (source_type, object_type, natural_key)
);

CREATE TABLE reference_object_revision (
    revision_id TEXT PRIMARY KEY,
    object_id TEXT NOT NULL REFERENCES reference_object(object_id),
    content_hash TEXT NOT NULL,
    payload_jsonb JSONB NOT NULL,
    valid_from_release_id TEXT NOT NULL REFERENCES reference_release(release_id),
    valid_to_release_id TEXT REFERENCES reference_release(release_id),
    operation TEXT NOT NULL CHECK (operation IN ('add', 'update', 'delete')),
    status TEXT NOT NULL,
    UNIQUE (object_id, content_hash, operation)
);

CREATE TABLE reference_change_set (
    change_id TEXT PRIMARY KEY,
    release_id TEXT NOT NULL REFERENCES reference_release(release_id),
    object_id TEXT NOT NULL REFERENCES reference_object(object_id),
    previous_revision_id TEXT REFERENCES reference_object_revision(revision_id),
    new_revision_id TEXT REFERENCES reference_object_revision(revision_id),
    change_type TEXT NOT NULL CHECK (change_type IN ('added', 'changed', 'deleted', 'unchanged')),
    change_summary TEXT,
    detected_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE reference_change_detail (
    change_detail_id TEXT PRIMARY KEY,
    change_id TEXT NOT NULL REFERENCES reference_change_set(change_id),
    field_path TEXT NOT NULL,
    change_type TEXT NOT NULL CHECK (change_type IN ('added', 'changed', 'deleted', 'unchanged')),
    old_value_hash TEXT,
    new_value_hash TEXT,
    old_value_preview TEXT,
    new_value_preview TEXT,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical'))
);

CREATE TABLE matching_rule_reference_dependency (
    rule_id TEXT NOT NULL,
    reference_object_id TEXT NOT NULL REFERENCES reference_object(object_id),
    reference_revision_id TEXT NOT NULL REFERENCES reference_object_revision(revision_id),
    dependency_type TEXT NOT NULL,
    required_review_on_change BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (rule_id, reference_object_id, reference_revision_id)
);

CREATE INDEX idx_reference_object_natural_key
    ON reference_object (source_type, object_type, natural_key);

CREATE INDEX idx_reference_revision_active_lookup
    ON reference_object_revision (object_id, valid_from_release_id, valid_to_release_id);

CREATE INDEX idx_reference_change_set_release
    ON reference_change_set (release_id, change_type);
