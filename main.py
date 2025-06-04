import argparse
import logging
import os
import pprint

from utils import file_utils
from utils.file_utils import load_file

from dotenv import load_dotenv

from config_loader import load_config, APP, set_config

load_dotenv()

parser = argparse.ArgumentParser(description="Ingest documents as Rag source")

parser.add_argument('--conf', type=str, help='Path to config file', required=False)
args = parser.parse_args()

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.debug("Arguments: {}".format(args))

# Create configuration
conf = load_config(args.conf)
set_config(conf)

from graph.graph import app

if  __name__ == '__main__':
    '''
    Counterpost
    '''

    original_post = load_file(conf[APP]['posting_path'])

    log.info("Counterpost")
    result = app.invoke(input={"posting": original_post})

    result_base_dir: str = conf.get(APP, "result_base_dir")
    os.makedirs(result_base_dir, exist_ok=True)

    file_utils.save_file(os.path.join(result_base_dir, "posting.txt"), result.get("posting"))
    file_utils.save_file(os.path.join(result_base_dir, "summary.txt"), result.get("summary"))

    if result.get("answer"):
        file_utils.save_file(os.path.join(result_base_dir, "neutral_answer.txt"), result.get("answer"))
        file_utils.save_file(os.path.join(result_base_dir, "final_answer.txt"), result.get("style_answer"))

        log.info(pprint.pformat(result["answer"]))
        log.info(pprint.pformat(result["style_answer"]))

    log.info("Program end")