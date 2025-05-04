from pprint import pprint

from dotenv import load_dotenv

load_dotenv()

from ingestion import retriever
from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader

def test_retrieval_grader_yes() -> None:
    question = "Ludwig"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "yes"
