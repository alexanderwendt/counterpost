import logging
from typing import Dict, Any

from config_loader import load_config, POSTING_WRITER_AGENT, IS_ACTIVATED, APP
from graph import state_utils
from graph.chains.posting_writer import posting_writer
from graph.consts import WRITE_ANSWER
from graph.state import GraphState

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

conf = load_config()
app_name: str = conf.get(APP, 'app_nickname')
is_activated: bool = conf.getboolean(POSTING_WRITER_AGENT, IS_ACTIVATED)

def write_posting(state: GraphState) -> Dict[str, Any]:
    log.info("---GENERATE ANSWER TO POSTING---")

    if is_activated:
        posting = state["posting"]
        summary = state["summary"]
        documents = state["filtered_value_documents"]

        answer = posting_writer.invoke({"posting": posting, "summary": summary, "value_documents": documents}).content

    else:
        answer = state_utils.load_state(app_name, WRITE_ANSWER)["answer"]

    log.debug("Counterpost without my style: {}".format(answer))
    return {"answer": answer}