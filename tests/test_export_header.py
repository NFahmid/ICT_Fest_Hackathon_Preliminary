"""Focused assertion for the exact CSV export header.

The manual (README, "Export CSV header (exact)") fixes the header string exactly.
Grading is black-box, so this guards the header against accidental drift.
"""
from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Exact contract string from README.md (underscores, no spaces).
EXPECTED_HEADER = "id,reference_code,room_id,user_id,start_time,end_time,status,price_cents"


def _admin_headers() -> dict:
    org = f"export-hdr-{datetime.now().timestamp()}"
    client.post("/auth/register", json={"org_name": org, "username": "admin", "password": "pw12345"})
    login = client.post("/auth/login", json={"org_name": org, "username": "admin", "password": "pw12345"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_export_csv_header_is_exact():
    resp = client.get("/admin/export", headers=_admin_headers())
    assert resp.status_code == 200
    header_line = resp.text.splitlines()[0]
    assert header_line == EXPECTED_HEADER
    assert " " not in header_line  # underscores, never spaces
