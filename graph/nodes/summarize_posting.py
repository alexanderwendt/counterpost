from graph.state import GraphState
from graph.chains.summarizer_chain import summarizer_chain


def summarize_posting(state: GraphState):
    print("---SUMMARIZE POSTING---")
    posting = state["posting"]

    summary = summarizer_chain.invoke(
        {"posting": posting}
    )

    return {
        "posting": posting,
        "summary": summary
    }
