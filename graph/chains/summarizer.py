from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config_loader import load_config, SUMMARIZER_AGENT, SYSTEM_PROMPT
from utils.file_utils import load_file

llm = ChatOpenAI(temperature=0)  # gpt 3.5

conf = load_config()
system_prompt = load_file(conf[SUMMARIZER_AGENT][SYSTEM_PROMPT])

#system_prompt = """
#    You are an intelligent summarization agent. Your task is to take a given posting as input and write a concise
#    summary of it. The purpose of this summary is to provide a reduced version of the posting that can be used as a
#    base for an answer to it. The summary should include all main claims and arguments, as well as any questions that
#    were asked in the posting. Remove any unnecessary details, redundant information, and irrelevant content.
#    Ensure that the summary is clear, coherent, and retains the essential points of the original posting. Provide
#    only the summary as an answer.
#    """

input_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{posting}"),
    ]
)

summarizer_chain = input_prompt | llm
