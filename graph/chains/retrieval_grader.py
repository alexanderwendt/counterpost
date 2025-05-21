from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from config_loader import load_config, VALUE_GRADER_AGENT, SYSTEM_PROMPT
from utils.file_utils import load_file

llm = ChatOpenAI(temperature=0)  # gpt 3.5

conf = load_config()
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

# system = """
#     You are a grader assessing the relevance of a document to a summary. The document will be used to create a counter
#     statement to a post. Check if the documents are related to each other, describing the same topic, answering the same
#     questions, also if their answers are opposing.
#
#     Parameters:
#     - Summary: The summarized post.
#     - Document: Document to check for relevance.
#
#     Instructions:
#     1. Identify Common Themes: Focus on identifying common themes or topics between the summary and the document, even
#     if they present opposing viewpoints. If they are opposing viewpoints, then the document is relevant to the summary.
#     2. Assess Relevance: Determine if the document addresses the same overarching topic or question as the summary, regardless of the stance taken.
#     3. Provide Binary Score: Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the summary.
#
#     Returns:
#     Binary score if the retrieved documents are relevant to the summary content, with the format 'yes' or 'no'.
#     In comments, you explain your decision.
#     """

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Document: \n\n {document} \n\n Summary: {summary}"),
    ]
)

# Take grade prompt, pipe it into the llm
retrieval_grader = grade_prompt | structured_llm_grader
