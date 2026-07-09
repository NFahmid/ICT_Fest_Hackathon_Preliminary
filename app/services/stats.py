"""Live per-room booking statistics.

Superseded in Phase 3: ``GET /rooms/{id}/stats`` now derives the confirmed count
and revenue directly from the database (see ``app/routers/rooms.py``), which is
always consistent with the bookings and safe under concurrency. This in-memory
module is retained only for backwards compatibility and is no longer wired into
any request path.
"""

_stats: dict[int, dict] = {}


def record_create(room_id: int, price_cents: int) -> None:
    current = _stats.get(room_id, {"count": 0, "revenue": 0})
    _stats[room_id] = {"count": current["count"] + 1, "revenue": current["revenue"] + price_cents}


def record_cancel(room_id: int, price_cents: int) -> None:
    current = _stats.get(room_id, {"count": 0, "revenue": 0})
    _stats[room_id] = {"count": max(0, current["count"] - 1), "revenue": current["revenue"] - price_cents}


def get(room_id: int) -> dict:
    return _stats.get(room_id, {"count": 0, "revenue": 0})
