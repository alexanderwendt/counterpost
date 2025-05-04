from graph.nodes.grade_documents import grade_documents
from langgraph.constants import END

from graph.nodes import retrieve_values
from graph.nodes.summarize_posting import summarize_posting
from graph.nodes.write_posting import write_posting
from graph.state import GraphState
from langgraph.graph import StateGraph

from graph.consts import ABORT, SUMMARIZE, RETRIEVE_VALUES, GRADE_DOCUMENTS, WRITE_ANSWER


def decide_to_answer(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if len(state["documents"]) == 0:
        print(
            "---DECISION: NO OPINION COULD BE FOUND TO THE FOLLOWING POST -> ABORT---"
        )
        return ABORT
    else:
        print("---DECISION: GENERATE ANSWER TO POSTING---")
        return WRITE_ANSWER


# Setup workflow
workflow = StateGraph(GraphState)
# Start
workflow.set_entry_point(SUMMARIZE)

# Nodes
workflow.add_node(SUMMARIZE, summarize_posting)
workflow.add_node(RETRIEVE_VALUES, retrieve_values)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(WRITE_ANSWER, write_posting)

# Value retriever
# Answer writer

# Edges
workflow.add_edge(SUMMARIZE, RETRIEVE_VALUES)
workflow.add_edge(RETRIEVE_VALUES, GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS,
                               decide_to_answer,
                               {
                                   ABORT: ABORT,
                                   WRITE_ANSWER: WRITE_ANSWER
                               }, )
# End
workflow.add_edge(WRITE_ANSWER, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="counterpost_graph.png")
