from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(temperature=0)  # gpt 3.5

system_prompt = """
    You are an intelligent summarization agent. Your task is to take a given posting as input and write a concise 
    summary of it. The purpose of this summary is to provide a reduced version of the posting that can be used as a 
    base for an answer to it. The summary should include all main claims and arguments, as well as any questions that 
    were asked in the posting. Remove any unnecessary details, redundant information, and irrelevant content. 
    Ensure that the summary is clear, coherent, and retains the essential points of the original posting. Provide
    only the summary as an answer.
    """

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{posting}"),
    ]
)

summarizer_chain = system_prompt | llm
