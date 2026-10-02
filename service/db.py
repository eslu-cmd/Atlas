"""Trusted-service Postgres connectivity for the M1 proof.

Uses psycopg 3 with Supabase's transaction pooler (port 6543). The connection
string carries the service-role database password — treat it as a secret, never
expose it to the browser.

Dictionary allocation and the write proof go through this module. The browser
cannot write directly to these tables (RLS rejects anon writes).
"""
from __future__ import annotations

import os
import contextlib
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row


def _dsn() -> str:
    dsn = os.environ.get("SUPABASE_DB_URL")
    if not dsn:
        raise RuntimeError("SUPABASE_DB_URL env var is not set")
    return dsn


@contextlib.contextmanager
def connect() -> Iterator[psycopg.Connection]:
    """Open a short-lived connection suitable for the transaction pooler."""
    conn = psycopg.connect(_dsn(), autocommit=False, prepare_threshold=None)
    try:
        yield conn
    finally:
        conn.close()


def allocate_token(
    *, namespace: str, scope: str, token: str, meaning: str, actor: str, reason: str
) -> dict[str, Any]:
    """Atomically allocate a dictionary token.

    Returns the stored row. If the (namespace, scope, token) slot is already
    taken, raises Conflict with the current meaning so the caller can decide
    whether to reuse or escalate.
    """
    with connect() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                insert into atlas_dictionary_tokens
                    (namespace, scope, token, meaning, allocated_by, reason)
                values (%s, %s, %s, %s, %s, %s)
                on conflict (namespace, scope, token) do nothing
                returning id, namespace, scope, token, meaning, allocated_by, reason, created_at
                """,
                (namespace, scope, token, meaning, actor, reason),
            )
            row = cur.fetchone()
            if row is None:
                cur.execute(
                    """
                    select id, namespace, scope, token, meaning, allocated_by, reason, created_at
                      from atlas_dictionary_tokens
                     where namespace=%s and scope=%s and token=%s
                    """,
                    (namespace, scope, token),
                )
                existing = cur.fetchone()
                conn.rollback()
                return {"status": "conflict", "existing": _jsonify(existing)}
        conn.commit()
    return {"status": "allocated", "row": _jsonify(row)}


def list_tokens() -> list[dict[str, Any]]:
    with connect() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                select id, namespace, scope, token, meaning, allocated_by, reason, created_at
                  from atlas_dictionary_tokens
                 order by created_at desc
                 limit 50
                """
            )
            return [_jsonify(r) for r in cur.fetchall()]


def write_proof(
    *,
    idempotency_key: str,
    payload: dict[str, Any],
    actor: str,
    reason: str,
    force_rollback: bool = False,
) -> dict[str, Any]:
    """Transactional write to atlas_m1_proof.

    - Normal path: inserts the row, commits, returns `inserted`.
    - Idempotent retry: same idempotency_key with the same payload returns the
      original row (`repeated`). Different payload for the same key fails.
    - `force_rollback=True`: inserts inside a transaction then raises so the
      caller can prove the row did NOT persist.
    """
    import json

    with connect() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                cur.execute(
                    """
                    insert into atlas_m1_proof (idempotency_key, payload, actor, reason)
                    values (%s, %s::jsonb, %s, %s)
                    returning id, idempotency_key, payload, actor, reason, created_at
                    """,
                    (idempotency_key, json.dumps(payload), actor, reason),
                )
                row = cur.fetchone()
                if force_rollback:
                    conn.rollback()
                    return {"status": "rolled_back", "attempted": _jsonify(row)}
                conn.commit()
                return {"status": "inserted", "row": _jsonify(row)}
            except psycopg.errors.UniqueViolation:
                conn.rollback()
                # Existing row for this idempotency_key — fetch and compare payload
                cur.execute(
                    """
                    select id, idempotency_key, payload, actor, reason, created_at
                      from atlas_m1_proof
                     where idempotency_key=%s
                    """,
                    (idempotency_key,),
                )
                existing = cur.fetchone()
                existing_json = _jsonify(existing)
                if existing_json["payload"] == payload:
                    return {"status": "repeated", "row": existing_json}
                return {"status": "payload_conflict", "existing": existing_json}


def row_exists(idempotency_key: str) -> bool:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select 1 from atlas_m1_proof where idempotency_key=%s", (idempotency_key,)
            )
            return cur.fetchone() is not None


def _jsonify(row: dict[str, Any] | None) -> dict[str, Any]:
    """Convert UUIDs and datetimes to strings so the row is JSON-serializable."""
    if row is None:
        return {}
    out: dict[str, Any] = {}
    for k, v in row.items():
        if hasattr(v, "isoformat"):
            out[k] = v.isoformat()
        elif isinstance(v, (bytes, bytearray)):
            out[k] = v.decode("utf-8", errors="replace")
        elif v is None or isinstance(v, (str, int, float, bool, list, dict)):
            out[k] = v
        else:
            out[k] = str(v)
    return out
