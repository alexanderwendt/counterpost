from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our total graph with intermediate results

    Attributes:
        posting: Original posting with statements to counter by writing an answer
        summary: Summarized version of the posting, reduced to only contain the core content
        value_documents: list of value document parts
        values: From our saved document find related topics
        generation: LLM generation
        web_search: whether to add a search
        documents: list of documents

    """

    posting: str
    summary: str
    value_documents: List[str]
    values: str
    answer: str