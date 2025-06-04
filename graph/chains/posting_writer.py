from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config_loader import load_config, POSTING_WRITER_AGENT, SYSTEM_PROMPT, get_config
from utils.file_utils import load_file

llm = ChatOpenAI(temperature=0) #gpt 3.5

conf = get_config()
system_prompt = load_file(conf[POSTING_WRITER_AGENT][SYSTEM_PROMPT])

input_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Posting begin:\n{posting}\n\nPosting End\n\nBegin Summary:\n{summary}\n\nEnd Summary\n\n"
                  "Begin Value documents:\n{value_documents}\n\nEnd Value documents"),
    ]
)

posting_writer = input_prompt | llm