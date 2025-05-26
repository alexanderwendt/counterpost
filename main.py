import argparse
import logging
import pprint
from utils.file_utils import load_file

from dotenv import load_dotenv

from config_loader import load_config, APP

load_dotenv()

from graph.graph import app

parser = argparse.ArgumentParser(description="Ingest documents as Rag source")

parser.add_argument('--conf', type=str, help='Path to config file', required=False)
args = parser.parse_args()

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.debug("Arguments: {}".format(args))

# Create configuration
conf = load_config(args.conf)


if  __name__ == '__main__':
    '''
    Counterpost
    '''

    original_post = load_file(conf[APP]['posting_path'])

    log.info("Counterpost")
    result = app.invoke(input={"posting": original_post})
    if result["answer"]:
        log.info(result["answer"])
        log.info(pprint.pformat(result["style_answer"]))

    log.info("Program end")