
import uuid
from datetime import datetime

def intake_node(state):
    # skip intake if resuming
    if state.get("resumed"):
        print("INTAKE skipped (resume)")
        return state
    # Read input
    payload = state.get("invoice_payload")

    if not payload:
        raise ValueError("invoice_payload is missing")

    # Minimal validation
    if "invoice_id" not in payload:
        raise ValueError("invoice_id is required")

    # Add metadata
    state["raw_id"] = str(uuid.uuid4())
    state["ingest_ts"] = datetime.utcnow().isoformat()

    print("INTAKE completed")

    return state
