from typing import Any, Dict

from langchain_community.embeddings import OpenAIEmbeddings

from config_loader import load_config
from graph import state_utils
from graph.consts import RETRIEVE_VALUES, RETRIEVE_STYLE
from graph.state import GraphState
from storage.customretriever import CustomChromaRetriever

agent_type = 'style_agent'
config = load_config("./conf/config.ini")

is_activated: bool = False


def retrieve_style(state: GraphState) -> Dict[str, Any]:
    '''
    Apply the loaded values on the post to write an answer

    :param state:
    :return:
    '''
    print("---GET RELEVANT STYLE FOR THE POST---")

    if is_activated:
        answer = state["answer"]
        retriever = CustomChromaRetriever(
            collection_name=config[agent_type]['collection_name'],
            persist_directory=config[agent_type]['persist_directory'],
            embedding_function=OpenAIEmbeddings(),
        ).as_retriever

        style_documents = retriever.invoke(answer)
    else:
        style_documents = state_utils.load_state(RETRIEVE_STYLE)["loaded_style_documents"]
    return {"loaded_style_documents": style_documents}
