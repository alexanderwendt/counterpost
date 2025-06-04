import logging

from config_loader import load_config, SUMMARIZER_AGENT, IS_ACTIVATED, APP, get_config
from graph import state_utils
from graph.state import GraphState
from graph.chains.summarizer import summarizer_chain

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Create configuration
conf = get_config()
app_name: str = conf.get(APP, 'app_nickname')
is_activated: bool = conf.getboolean(SUMMARIZER_AGENT, IS_ACTIVATED)


def summarize_posting(state: GraphState):
    log.info("---SUMMARIZE POSTING---")
    posting = state["posting"]

    if is_activated:
        summary = summarizer_chain.invoke(
            {"posting": posting}
        ).content
    else:
        log.warning("Module deactivated. Load from state SUMMARIZE")
        summary = state_utils.load_state(app_name, "SUMMARIZE")["summary"]

    log.debug("Posting:\n{}, \nSummary: \n{}".format(posting, summary))

    return {"summary": summary}
