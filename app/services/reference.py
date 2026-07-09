"""Human-facing booking reference codes.

Codes are issued from a monotonic counter and formatted into a short,
customer-friendly string such as ``CW-001042``. Issuance is guarded by a lock
so codes stay unique under concurrent booking creation.
"""
import threading

_counter = {"value": 1000}
_lock = threading.Lock()


def next_reference_code() -> str:
    with _lock:
        current = _counter["value"]
        _counter["value"] = current + 1
    return f"CW-{current:06d}"
