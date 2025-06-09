from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.llms import OllamaLLM

def get_rag_chain():
    template = """Answer the question using ONLY the following verified facts. 
    Be precise and include relevant snippets from the context:

    Context:
    {context}

    Question: {question}

    Provide a detailed answer with source references in this format:
    [Source 1] Relevant snippet from context
    [Source 2] Relevant snippet from context
    ..."""
    
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3", temperature=0.3)  # Lower temp for factual answers
    
    return (
        {
            "context": RunnablePassthrough(),
            "question": RunnablePassthrough()
        } 
        | prompt 
        | model
    )