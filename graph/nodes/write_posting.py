import logging
from typing import Dict, Any

from config_loader import load_config, POSTING_WRITER_AGENT, IS_ACTIVATED
from graph import state_utils
from graph.chains.posting_writer import posting_writer
from graph.consts import WRITE_ANSWER
from graph.state import GraphState

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

conf = load_config()
is_activated: bool = conf.getboolean(POSTING_WRITER_AGENT, IS_ACTIVATED)

def write_posting(state: GraphState) -> Dict[str, Any]:
    log.info("---GENERATE ANSWER TO POSTING---")

    if is_activated:
        posting = state["summary"]
        documents = state["filtered_value_documents"]

        answer = posting_writer.invoke({"value_documents": documents, "posting": posting}).content

    else:
        answer = state_utils.load_state(WRITE_ANSWER)["answer"]

    log.debug("Counterpost without my style: {}".format(answer))
    return {"answer": answer}