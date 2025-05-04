import os

from langchain_chroma import Chroma


class CustomChromaRetriever:
    '''
    Retriever from Chroma

    '''

    def __init__(self, collection_name, persist_directory, embedding_function):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self.as_retriever = self.initialize_retriever()

    def initialize_retriever(self):
        if not os.path.exists(self.persist_directory):
            print(f"Warning: No repository loaded in the specified directory '{self.persist_directory}'.")
        else:
            print("Repository loaded successfully.")
        return Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function,
        ).as_retriever()
