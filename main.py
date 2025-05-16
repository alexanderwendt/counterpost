import argparse
import logging
import pprint

from dotenv import load_dotenv

from config_loader import load_config, APP

load_dotenv()

from graph.graph import app

parser = argparse.ArgumentParser(description="Ingest documents as Rag source")

parser.add_argument('--conf', type=str, help='Path to config file', required=True)
args = parser.parse_args()

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.debug("Arguments: {}".format(args))

# Create configuration
config = load_config(args.conf)


def load_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


if  __name__ == '__main__':
    '''
    Counterpost
    '''

    original_post = load_file(config[APP]['posting_path'])

    log.info("Counterpost")
    result = app.invoke(input={"posting": original_post})
    log.info(result["answer"])
    log.info(pprint.pformat(result["style_answer"]))

    log.info("Program end")