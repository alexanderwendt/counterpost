from typing import Any, Dict

from langchain_community.embeddings import OpenAIEmbeddings

from config_loader import load_config
from graph.state import GraphState
from storage.customretriever import CustomChromaRetriever

agent_type = 'value_agent'
config = load_config("./conf/config.ini")

def apply_values(state: GraphState) -> Dict[str, Any]:
    '''
    Apply the loaded values on the post to write an answer

    :param state:
    :return:
    '''
    print("---GET RELEVANT OWN VALUES ON THE POST---")
    summary = state["summary"]

    retriever = CustomChromaRetriever(
        collection_name=config[agent_type]['collection_name'],
        persist_directory=config[agent_type]['persist_directory'],
        embedding_function=OpenAIEmbeddings(),
    ).as_retriever

    value_documents = retriever.invoke(summary)
    return {"value_documents": value_documents, "summary": summary, "posting": state["posting"]}
