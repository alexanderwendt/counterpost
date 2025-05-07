import logging

from config_loader import load_config
from graph import state_utils
from graph.state import GraphState
from graph.chains.summarizer_chain import summarizer_chain

# Create configuration
config = load_config("./conf/config.ini")
is_activated = True

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def summarize_posting(state: GraphState):
    log.info("---SUMMARIZE POSTING---")
    posting = state["posting"]

    if is_activated:
        summary = summarizer_chain.invoke(
            {"posting": posting}
        ).content
    else:
        log.warning("Module deactivated. Load from state SUMMARIZE")
        summary = state_utils.load_state("SUMMARIZE")["summary"]

    log.debug("Posting:\n{}, \nSummary: \n{}".format(posting, summary))

    return {
        "posting": posting,
        "summary": summary
    }
