from typing import Any, Dict

from langchain_community.embeddings import OpenAIEmbeddings

from config_loader import load_config, IS_ACTIVATED, STYLE_RETRIEVER_AGENT
from graph import state_utils
from graph.consts import RETRIEVE_VALUES, RETRIEVE_STYLE
from graph.state import GraphState
from storage.customretriever import CustomChromaRetriever

conf = load_config()
is_activated: bool = conf.getboolean(STYLE_RETRIEVER_AGENT, IS_ACTIVATED)


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
            collection_name=conf[STYLE_RETRIEVER_AGENT]['collection_name'],
            persist_directory=conf[STYLE_RETRIEVER_AGENT]['persist_directory'],
            embedding_function=OpenAIEmbeddings(),
        ).as_retriever

        style_documents = retriever.invoke(answer)
    else:
        style_documents = state_utils.load_state(RETRIEVE_STYLE)["loaded_style_documents"]
    return {"loaded_style_documents": style_documents}
