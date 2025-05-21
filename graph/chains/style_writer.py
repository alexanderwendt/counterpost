from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config_loader import load_config, SYSTEM_PROMPT, STYLE_WRITER_AGENT
from utils.file_utils import load_file

llm = ChatOpenAI(temperature=0) #gpt 3.5

conf = load_config()
system_prompt = load_file(conf[STYLE_WRITER_AGENT][SYSTEM_PROMPT])

#system_prompt = """
#        You are a style transfer assistant. Your task is to rewrite a given text ("posting") using only
#        the **style** of another document ("Style documents"). Do not copy content or meaning from the style documents.
#        Use only its tone, vocabulary, sentence structure, and stylistic features.
#        For example, if the style documents are written in shakespearean style, rewrite the posting in shakespearean speak, even if the topics
#        are unrelated. Be creative and consistent in applying
#        the style. Output only the rewritten version of the posting.
#                 """

input_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Posting: {posting}, Style documents: {loaded_style_documents}"),
    ]
)

style_writer = input_prompt | llm