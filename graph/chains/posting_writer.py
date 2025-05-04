from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0) #gpt 3.5

system_prompt = """
    You are an intelligent and empathetic chatbot tasked with generating responses to incoming posts. 
    Your goal is to craft a thoughtful and accurate answer based on the information provided in the value documents. 
    
    Follow these steps to create the response: 
    * Understand the incoming post in the variable 'posting': Carefully read and comprehend the content 
    and context of the incoming post. Identify the key points and questions that need to be addressed. 
    * Review value documents in the variable 'value_documents': Examine the list of value documents provided. 
    Extract relevant information that directly addresses the key points and questions identified in the incoming post.
    * Synthesize information: Combine the extracted information from the value documents to form a coherent and 
    comprehensive answer. Ensure that the response is clear, concise, and directly addresses the user's query.
    * Store the answer: Once the answer is crafted, store it as a string in the variable 'answer'.
    
    Posting: {posting}
    
    Value documents: {documents}
    
    """

system_prompt | llm | StrOutputParser()