import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, store_in_chromadb
from parse import get_rag_chain

st.title("NaviQA (RAG-Enhanced)")
url = st.text_input("Enter a Website URL:")

if st.button("Scrape Site"):
    st.write("Scraping the website...")
    html = scrape_website(url)
    body_content = extract_body_content(html)
    cleaned_content = clean_body_content(body_content)
    
    # Store in ChromaDB and get retriever
    retriever = store_in_chromadb(cleaned_content)
    st.session_state.retriever = retriever
    
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "retriever" in st.session_state:
    parse_description = st.text_area("What information do you want to extract?")
    
    if st.button("Parse Content"):
        if parse_description:
            st.write("Generating RAG-powered response...")
            rag_chain = get_rag_chain(st.session_state.retriever)
            response = rag_chain.invoke(parse_description)
            st.write(response)