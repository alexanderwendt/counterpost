from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
    :param state: state(dict), the current graph state
    :return: state(dict), filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT OF RELEVANCE TO POSTING---")
    query = state["summary"]
    documents = state["value_documents"]

    filtered_docs = []
    for d in documents:
        score = retrieval_grader.invoke(
            {"query": query, "document": d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: VALUE DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: VALUE DOCUMENT NOT RELEVANT, SKIP---")
            continue
    return {"value_documents": filtered_docs, "summary": query}