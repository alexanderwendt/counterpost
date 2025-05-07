import logging

from langgraph.constants import END
from langgraph.graph import StateGraph

from graph import state_utils
from graph.consts import ABORT, SUMMARIZE, RETRIEVE_VALUES, GRADE_DOCUMENTS, WRITE_ANSWER
from graph.nodes.grade_documents import grade_documents
from graph.nodes.retrieve_values import retrieve_values
from graph.nodes.summarize_posting import summarize_posting
from graph.nodes.write_posting import write_posting
from graph.state import GraphState

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


# Function to print the output of each node
def print_node_output(node_name, node_function, *args, **kwargs):
    output = node_function(*args, **kwargs)
    state_utils.save_state(output, node_name)
    log.debug(f"Output of {node_name}: {output}")
    return output


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
workflow.add_node(SUMMARIZE, lambda *args, **kwargs: print_node_output(SUMMARIZE, summarize_posting, *args, **kwargs))
workflow.add_node(RETRIEVE_VALUES, lambda *args, **kwargs: print_node_output(RETRIEVE_VALUES, retrieve_values, *args, **kwargs))
workflow.add_node(GRADE_DOCUMENTS, lambda *args, **kwargs: print_node_output(GRADE_DOCUMENTS, grade_documents, *args, **kwargs))
workflow.add_node(WRITE_ANSWER, lambda *args, **kwargs: print_node_output(WRITE_ANSWER, write_posting, *args, **kwargs))

# Value retriever
# Answer writer

# Edges
workflow.add_edge(SUMMARIZE, RETRIEVE_VALUES)
workflow.add_edge(RETRIEVE_VALUES, GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS,
                               decide_to_answer,
                               {
                                   ABORT: END,
                                   WRITE_ANSWER: WRITE_ANSWER
                               }, )
# End
workflow.add_edge(WRITE_ANSWER, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="counterpost_graph.png")
