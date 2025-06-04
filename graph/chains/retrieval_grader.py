from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from config_loader import load_config, VALUE_GRADER_AGENT, SYSTEM_PROMPT, get_config
from utils.file_utils import load_file

llm = ChatOpenAI(temperature=0)  # gpt 3.5

conf = get_config()
system_prompt = load_file(conf[VALUE_GRADER_AGENT][SYSTEM_PROMPT])

class GradeDocuments(BaseModel):
    """
    Binary score for relevance check on retireved documents.
    """

    binary_score: str = Field(
        description="Retrieved documents are relevant to the question, 'yes' or 'no'"
    )
    comment: str = Field(
        description="Description why the score was decided to be yes or no"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Begin Summary: {summary}\n\nEnd Summary\n============================================="
                  "\n\nBegin My position: \n\n {my_position}\n\nEnd My position"),
    ]
)

# Take grade prompt, pipe it into the llm
retrieval_grader = grade_prompt | structured_llm_grader
