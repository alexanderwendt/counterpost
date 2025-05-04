from typing import Dict, Any

from graph.chains import posting_writer
from graph.state import GraphState


def write_posting(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE ANSWER TO POSTING---")
    posting = state["summary"]
    documents = state["value_documents"]

    answer = posting_writer.invoke({"documents": documents, "posting": posting})
    return {"value_documents": documents, "summary": posting, "answer": answer}