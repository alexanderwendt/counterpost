from typing import Any, Dict

from langchain_community.embeddings import OpenAIEmbeddings

from config_loader import load_config
from graph import state_utils
from graph.consts import RETRIEVE_VALUES
from graph.state import GraphState
from storage.customretriever import CustomChromaRetriever

agent_type = 'value_agent'
config = load_config("./conf/config.ini")

is_activated: bool = True

def retrieve_values(state: GraphState) -> Dict[str, Any]:
    '''
    Apply the loaded values on the post to write an answer

    :param state:
    :return:
    '''
    print("---GET RELEVANT OWN VALUES ON THE POST---")
    summary = state["summary"]

    if is_activated:
        retriever = CustomChromaRetriever(
            collection_name=config[agent_type]['collection_name'],
            persist_directory=config[agent_type]['persist_directory'],
            embedding_function=OpenAIEmbeddings(),
        ).as_retriever

        value_documents = retriever.invoke(summary)
    else:
        value_documents = state_utils.load_state(RETRIEVE_VALUES)["loaded_value_documents"]
    return {"loaded_value_documents": value_documents}
