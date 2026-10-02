-- Atlas records 0.2.1: immutable nodes and ordered, foreign-key-backed edges.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS records (
 id TEXT PRIMARY KEY, kind TEXT NOT NULL, data TEXT NOT NULL CHECK(json_valid(data)),
 actor TEXT NOT NULL CHECK(length(actor)>0), recorded_at TEXT NOT NULL,
 reason TEXT NOT NULL CHECK(length(reason)>0), effective_at TEXT,
 provenance TEXT NOT NULL CHECK(provenance IN ('source','illustrative','operational'))
);
CREATE TABLE IF NOT EXISTS links (
 owner TEXT NOT NULL REFERENCES records(id), role TEXT NOT NULL,
 position INTEGER NOT NULL CHECK(position>=0), target TEXT NOT NULL REFERENCES records(id),
 PRIMARY KEY(owner,role,position)
);
CREATE INDEX IF NOT EXISTS records_kind ON records(kind);
CREATE INDEX IF NOT EXISTS links_target ON links(target,role);
CREATE TABLE IF NOT EXISTS unique_keys (
 namespace TEXT NOT NULL, value TEXT NOT NULL, record TEXT NOT NULL REFERENCES records(id),
 PRIMARY KEY(namespace,value)
);
CREATE TRIGGER IF NOT EXISTS records_no_update BEFORE UPDATE ON records BEGIN SELECT RAISE(ABORT,'Records are immutable'); END;
CREATE TRIGGER IF NOT EXISTS records_no_delete BEFORE DELETE ON records BEGIN SELECT RAISE(ABORT,'Records are immutable'); END;
CREATE TRIGGER IF NOT EXISTS links_no_update BEFORE UPDATE ON links BEGIN SELECT RAISE(ABORT,'Links are immutable'); END;
CREATE TRIGGER IF NOT EXISTS links_no_delete BEFORE DELETE ON links BEGIN SELECT RAISE(ABORT,'Links are immutable'); END;
CREATE TRIGGER IF NOT EXISTS keys_no_update BEFORE UPDATE ON unique_keys BEGIN SELECT RAISE(ABORT,'Keys are immutable'); END;
CREATE TRIGGER IF NOT EXISTS keys_no_delete BEFORE DELETE ON unique_keys BEGIN SELECT RAISE(ABORT,'Keys are immutable'); END;
PRAGMA user_version = 1;
