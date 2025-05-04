import argparse

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
import logging

from config_loader import load_config
from customretriever import CustomChromaRetriever

load_dotenv()

parser = argparse.ArgumentParser(description="Ingest documents as Rag source")

parser.add_argument('--conf', type=str, help='Path to config file', required=True)
parser.add_argument('--repo', type=str, help='Config Section for the RAG', required=True)
parser.add_argument('-l', '--load', action='store_true', help="Load from files into RAG storage")
args = parser.parse_args()

# Create a custom logger
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.debug("Arguments: {}".format(args))

# Create configuration
config = load_config(args.conf)


class Ingestion:
    def __init__(self, config_section: str, config):
        self.config_section = config_section
        self.config = config
        log.info("Load ingestor")

    def ingest(self, do_load: bool = True) -> None:
        urls = [
            "https://orf.at/stories/3386196/",
            "https://orf.at/stories/3386199/",
            "https://orf.at/stories/3385391/"
        ]

        # paths = [
        #    "./resources/pirate_style_doc.txt"
        # ]

        paths = config[self.config_section]['ingest_paths'].split(',')

        # docs = [WebBaseLoader(url).load() for url in urls]
        docs = [TextLoader(path, encoding='utf-8').load() for path in paths]
        docs_list = [item for sublist in docs for item in sublist]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )

        doc_splits = text_splitter.split_documents(docs_list)

        if do_load:
            print("Load files")
            vectorstore = Chroma.from_documents(
                documents=doc_splits,
                collection_name=config[self.config_section]['collection_name'],
                embedding=OpenAIEmbeddings(),
                persist_directory=config[self.config_section]['persist_directory']
            )


if __name__ == '__main__':
    print("Hello Advanced RAG")
    ingestor = Ingestion(args.repo, config)
    ingestor.ingest(args.load)

    retriever = CustomChromaRetriever(
        collection_name=config[args.repo]['collection_name'],
        persist_directory=config[args.repo]['persist_directory'],
        embedding_function=OpenAIEmbeddings(),
    ).as_retriever

    test_prompt = """
        Write the following text in the style of the retrieved documents: 
        Massive power outage: Large parts of Spain and Portugal experienced major power outages, shutting off traffic lights and causing chaos at travel hubs. In Spain, all rail traffic has come to a halt and in Portugal, authorities are warning against any unnecessary travel due to the risk of traffic lights failing.
        """
    valueList = retriever.invoke("""
        How many rings do Jupiter have?
        """)
    print(valueList)
