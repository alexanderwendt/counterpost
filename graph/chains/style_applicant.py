from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0) #gpt 3.5

system_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                 to answer the question. If you don't know the answer, just say that you don't know. 
                 Use three sentences maximum and keep the answer concise.
                 Question: {question}
                 Context: {context}
                 Answer:"""

#style_chain = system_prompt | llm |