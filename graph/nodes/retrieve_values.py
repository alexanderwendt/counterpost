from typing import Any, Dict

from langchain_community.embeddings import OpenAIEmbeddings

from config_loader import load_config, VALUE_RETRIEVAL_AGENT, IS_ACTIVATED, APP
from graph import state_utils
from graph.consts import RETRIEVE_VALUES
from graph.state import GraphState
from storage.customretriever import CustomChromaRetriever

conf = load_config()
app_name: str = conf.get(APP, 'app_nickname')
is_activated: bool = conf.getboolean(VALUE_RETRIEVAL_AGENT, IS_ACTIVATED)

def retrieve_values(state: GraphState) -> Dict[str, Any]:
    '''
    Apply the loaded values on the post to write an answer

    :param state:
    :return:
    '''
    print("---GET RELEVANT OWN VALUES ON THE POST---")

    if is_activated:
        summary = state["summary"]
        retriever = CustomChromaRetriever(
            collection_name=conf[VALUE_RETRIEVAL_AGENT]['collection_name'],
            persist_directory=conf[VALUE_RETRIEVAL_AGENT]['persist_directory'],
            embedding_function=OpenAIEmbeddings(),
        ).as_retriever

        value_documents = retriever.invoke(summary)
    else:
        value_documents = state_utils.load_state(app_name, RETRIEVE_VALUES)["loaded_value_documents"]
    return {"loaded_value_documents": value_documents}
