from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.llms import OllamaLLM

def get_rag_chain(retriever):
    template = """
    You are a website content analyzer. Use the following context to answer the question.
    
    Context: {context}
    
    Question: {parse_description}
    
    Provide a detailed summary or extract specific information as requested.
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    model = OllamaLLM(model="llama3.2")
    
    return (
        {"context": retriever, "parse_description": RunnablePassthrough()} 
        | prompt 
        | model
    )