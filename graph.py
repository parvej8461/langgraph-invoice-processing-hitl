

from langgraph.graph import StateGraph, END
from state import InvoiceState

from nodes.intake import intake_node
from nodes.understand import understand_node
from nodes.match import match_node
from nodes.checkpoint import checkpoint_node


# Routing logic after MATCH
def route_after_match(state):
    # If resuming after human approval, do NOT checkpoint again
    if state.get("resumed") and state.get("human_decision") == "ACCEPT":
        print("Routing: resume approved → END")
        return END

    # Normal HITL path
    if state["match_result"] == "FAILED":
        print("Routing: match failed → CHECKPOINT")
        return "CHECKPOINT"

    return END



def build_graph():
    graph = StateGraph(InvoiceState)

    # Register nodes
    graph.add_node("INTAKE", intake_node)
    graph.add_node("UNDERSTAND", understand_node)
    graph.add_node("MATCH", match_node)
    graph.add_node("CHECKPOINT", checkpoint_node)

    # Entry point
    graph.set_entry_point("INTAKE")

    # Normal flow
    graph.add_edge("INTAKE", "UNDERSTAND")
    graph.add_edge("UNDERSTAND", "MATCH")

    # Conditional flow
    graph.add_conditional_edges(
        "MATCH",
        route_after_match,
        {
            "CHECKPOINT": "CHECKPOINT",
            END: END
        }
    )

    return graph.compile()
