from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0) #gpt 3.5

system_prompt = """You are an my personal assistant for transforming a text to sound as it was written by me. 
                 The document to process and to rewrite ist in the variable 'posting'. The style, which you shall 
                 use to rewrite the text ist provided as a list of documents in the variable 'Style documents'. You returns
                 the processed text.
                 """

input_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Posting: {posting}, Style documents: {loaded_style_documents}"),
    ]
)

style_writer = input_prompt | llm