from bigtool import bigtool_picker

def understand_node(state):
    if state.get("resumed"):
        print("UNDERSTAND skipped (resume)")
        return state
    
    # Bigtool selection
    ocr_tool = bigtool_picker(capability="ocr",
        context={"file_type": "pdf"}
    )


    print(f"Bigtool selected OCR provider: {ocr_tool}")

    # Mock OCR + parsing result
    state["parsed_invoice"] = {
        "invoice_number": state["invoice_payload"]["invoice_id"],
        "total_amount": 1200,
        "currency": "INR",
        "line_items": [
            {
                "description": "Item A",
                "quantity": 2,
                "unit_price": 500,
                "total": 1000
            }
        ]
    }

    print("OCR and parsing completed")

    return state
