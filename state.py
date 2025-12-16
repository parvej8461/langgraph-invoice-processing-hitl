from typing import TypedDict, Optional

class InvoiceState(TypedDict, total=False):
    # Original input
    invoice_payload: dict

    # Intake stage
    raw_id: str
    ingest_ts: str

    # OCR / Understanding stage
    parsed_invoice: dict

    # Matching stage
    match_score: float
    match_result: str

    # Human-in-the-loop
    hitl_checkpoint_id: Optional[str]
    human_decision: Optional[str]
    resumed: Optional[bool]

