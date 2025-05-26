from typing import Any, Dict

import logging

from config_loader import load_config, IS_ACTIVATED, VALUE_GRADER_AGENT
from graph.consts import GRADE_DOCUMENTS

from graph import state_utils
from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

conf = load_config()
is_activated: bool = conf.getboolean(VALUE_GRADER_AGENT, IS_ACTIVATED)

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
    :param state: state(dict), the current graph state
    :return: state(dict), filtered out irrelevant documents and updated web_search state
    """

    log.info("---CHECK DOCUMENT OF RELEVANCE TO POSTING---")

    if is_activated:
        query = state["summary"]
        documents = state["loaded_value_documents"]

        filtered_docs = []
        for d in documents:
            document: str = d.page_content
            score = retrieval_grader.invoke(
                {"summary": query, "document": document}
            )
            grade = score.binary_score
            if grade.lower() == "yes":
                log.info("---GRADE: VALUE DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                log.info("---GRADE: VALUE DOCUMENT NOT RELEVANT, SKIP---")
            log.debug("Grading comment: {}".format(score.comment))
    else:
        filtered_docs = state_utils.load_state(GRADE_DOCUMENTS)["filtered_value_documents"]
    return {"filtered_value_documents": filtered_docs}