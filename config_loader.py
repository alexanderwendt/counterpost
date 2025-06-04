import configparser
import logging
import os

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

env_path_variable: str = "COUNTERPOST_CONFIG_PATH"

APP = "app"
SUMMARIZER_AGENT = 'summarizer_agent'
VALUE_RETRIEVAL_AGENT = 'value_retrieval_agent'
VALUE_GRADER_AGENT = 'value_grader_agent'
POSTING_WRITER_AGENT = 'posting_writer_agent'
STYLE_RETRIEVER_AGENT = 'style_retriever_agent'
STYLE_WRITER_AGENT = 'style_writer_agent'

SYSTEM_PROMPT = 'system_prompt'
IS_ACTIVATED = 'is_activated'


def load_config(file_path: str = None):
    '''
    Load config

    :param file_path:
    :return:
    '''
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    if file_path:
        log.info("Load config from file: {}".format(file_path))
        os.environ[env_path_variable] = file_path
    else:
        log.debug("Load config from default path in .env. Path: {}".format(os.environ[env_path_variable]))

    with open(os.getenv(env_path_variable), encoding='utf-8') as f:
        config.read_file(f)

    return config


def set_config(conf):
    global config
    config = conf

def get_config():
    return config

