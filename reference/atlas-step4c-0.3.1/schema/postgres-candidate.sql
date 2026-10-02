-- UNEXECUTED Postgres translation of the local storage substrate, not a Supabase deployment.
-- The Python Store contracts must be ported as a trusted service/transaction layer.
-- Do not grant direct client writes to these tables. No RLS/auth/storage policy is supplied.
CREATE TABLE atlas_records (
 id text PRIMARY KEY, kind text NOT NULL, data jsonb NOT NULL,
 actor text NOT NULL CHECK(length(actor)>0), recorded_at timestamptz NOT NULL,
 reason text NOT NULL CHECK(length(reason)>0), effective_at timestamptz,
 provenance text NOT NULL CHECK(provenance IN ('source','illustrative','operational'))
);
CREATE TABLE atlas_links (
 owner text NOT NULL REFERENCES atlas_records(id), role text NOT NULL,
 position integer NOT NULL CHECK(position>=0), target text NOT NULL REFERENCES atlas_records(id),
 PRIMARY KEY(owner,role,position)
);
CREATE INDEX atlas_records_kind ON atlas_records(kind);
CREATE INDEX atlas_links_target ON atlas_links(target,role);
CREATE TABLE atlas_unique_keys (
 namespace text NOT NULL, value text NOT NULL, record text NOT NULL REFERENCES atlas_records(id),
 PRIMARY KEY(namespace,value)
);
CREATE FUNCTION atlas_refuse_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'Atlas snapshots are immutable; append a revision/correction'; END;
$$;
CREATE TRIGGER atlas_records_immutable BEFORE UPDATE OR DELETE ON atlas_records FOR EACH ROW EXECUTE FUNCTION atlas_refuse_mutation();
CREATE TRIGGER atlas_links_immutable BEFORE UPDATE OR DELETE ON atlas_links FOR EACH ROW EXECUTE FUNCTION atlas_refuse_mutation();
CREATE TRIGGER atlas_keys_immutable BEFORE UPDATE OR DELETE ON atlas_unique_keys FOR EACH ROW EXECUTE FUNCTION atlas_refuse_mutation();
