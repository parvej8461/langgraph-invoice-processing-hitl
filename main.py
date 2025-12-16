import sqlite3
import json
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from graph import build_graph

graph = build_graph()

app = FastAPI()

# Resume workflow from checkpoint

def resume_from_checkpoint(checkpoint_id: str, decision: str):
    """
    Loads workflow state from DB and resumes LangGraph execution
    after human ACCEPT / REJECT decision.
    """

    conn = sqlite3.connect("db/demo.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT state_json FROM checkpoints WHERE checkpoint_id = ?",
        (checkpoint_id,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise ValueError("Checkpoint not found")

    state = json.loads(row[0])

    # Inject human decision
    state["human_decision"] = decision
    state["resumed"] = True

    print("\nResuming workflow with human decision:", decision)

    return graph.invoke(state)


# Human Review UI (GET)

@app.get("/human-review", response_class=HTMLResponse)
def human_review_ui():
    conn = sqlite3.connect("db/demo.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT checkpoint_id, state_json FROM checkpoints WHERE status='PENDING'"
    )
    rows = cur.fetchall()
    conn.close()

    html = "<h2>Pending Invoice Reviews</h2>"

    if not rows:
        html += "<p>No pending invoices.</p>"
        return html

    for checkpoint_id, state_json in rows:
        state = json.loads(state_json)

        html += f"""
        <div style="border:1px solid #ccc; padding:10px; margin:10px;">
            <p><b>Invoice ID:</b> {state['invoice_payload']['invoice_id']}</p>
            <p><b>Amount:</b> {state['invoice_payload']['amount']}</p>
            <p><b>Currency:</b> {state['invoice_payload']['currency']}</p>
            <p><b>Match Score:</b> {state['match_score']}</p>

            <form method="post" action="/human-review/decision">
                <input type="hidden" name="checkpoint_id" value="{checkpoint_id}">
                <button name="decision" value="ACCEPT">ACCEPT</button>
                <button name="decision" value="REJECT">REJECT</button>
            </form>
        </div>
        """

    return html


# Handle Human Decision (POST)
@app.post("/human-review/decision")
def submit_decision(
    checkpoint_id: str = Form(...),
    decision: str = Form(...)
):
    conn = sqlite3.connect("db/demo.db")
    cur = conn.cursor()

    # Update checkpoint status
    cur.execute(
        "UPDATE checkpoints SET status=? WHERE checkpoint_id=?",
        (decision, checkpoint_id)
    )
    conn.commit()
    conn.close()

    # Resume LangGraph workflow
    resume_from_checkpoint(checkpoint_id, decision)

    return {"message": f"Invoice {decision}ED successfully"}


# ---------------------------------------------------------
# Run workflow directly (CLI execution)

if __name__ == "__main__":
    input_state = {
        "invoice_payload": {
            "invoice_id": "INV-002",
            "amount": 1200,
            "currency": "INR"
        }
    }

    result = graph.invoke(input_state)

    print("\nFINAL STATE:")
    print(result)
