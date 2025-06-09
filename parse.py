from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.llms import OllamaLLM

def get_rag_chain():
    template = """Answer using these verified facts:
{context}

Question: {question}
Include source snippets in your answer."""
    
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3")
    
    return (
        {
            "context": RunnablePassthrough(),
            "question": RunnablePassthrough()
        } 
        | prompt 
        | model
    )