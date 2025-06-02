import logging
from typing import Dict, Any

from config_loader import load_config, STYLE_WRITER_AGENT, IS_ACTIVATED, APP
from graph import state_utils
from graph.chains.posting_writer import posting_writer
from graph.chains.style_writer import style_writer
from graph.consts import WRITE_ANSWER, WRITE_STYLE
from graph.state import GraphState

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

conf = load_config()
app_name: str = conf.get(APP, 'app_nickname')
is_activated: bool = conf.getboolean(STYLE_WRITER_AGENT, IS_ACTIVATED)

def write_style(state: GraphState) -> Dict[str, Any]:
    log.info("---APPLY MY STYLE TO THE POSTING---")

    if is_activated:
        posting = state["answer"]
        documents = state["loaded_style_documents"]

        style_answer = style_writer.invoke({"loaded_style_documents": documents, "posting": posting}).content
    else:
        style_answer = state_utils.load_state(app_name, WRITE_STYLE)["style_answer"]

    log.debug("Counterpost with my style: {}".format(style_answer))
    return {"style_answer": style_answer}
