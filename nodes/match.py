
from bigtool import bigtool_picker

def match_node(state):

    if state.get("resumed"):
        print("MATCH skipped (resume)")
        return state

    #Bigtool selection
    erp_tool = bigtool_picker(capability="erp",
        context={"env": "demo"}
    )

    print(f"Bigtool selected ERP provider: {erp_tool}")

    # print("MATCH started")

    # Invoice amount from OCR stage
    invoice_amount = state["parsed_invoice"]["total_amount"]

    # Mock PO amount (pretend fetched from ERP)
    po_amount = 2000

    # Simple match score
    match_score = invoice_amount / po_amount

    state["match_score"] = round(match_score, 2)

    if match_score >= 0.90:
        state["match_result"] = "MATCHED"
    else:
        state["match_result"] = "FAILED"

    print(f"MATCH score: {state['match_score']} → {state['match_result']}")

    return state
