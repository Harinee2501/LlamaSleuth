import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, store_in_chromadb
from parse import get_rag_chain
import sys
import asyncio

# Configuration
st.set_page_config(layout="wide")
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# App UI
st.title("🦙 LlamaSleuth - Advanced Web Analyzer")
url = st.text_input("Enter a Website URL:", placeholder="https://example.com")

if st.button("Scrape Site"):
    if not url.startswith(('http://', 'https://')):
        st.error("Please enter a valid URL starting with http:// or https://")
    else:
        with st.spinner("🔍 Scraping the website..."):
            try:
                html = scrape_website(url)
                body_content = extract_body_content(html)
                cleaned_content = clean_body_content(body_content)

                retriever = store_in_chromadb(cleaned_content, url)

                if retriever is not None:
                    st.session_state.retriever = retriever
                    st.session_state.content = cleaned_content
                    st.success("✅ Website scraped successfully!")
                    with st.expander("View DOM Content"):
                        st.text_area("DOM Content", cleaned_content, height=300)
                else:
                    st.error("❌ Failed to initialize retriever. Content may be empty or malformed.")
            except Exception as e:
                st.error(f"❌ Scraping failed: {str(e)}")

if "retriever" in st.session_state:
    st.divider()
    st.subheader("Ask Questions About the Content")
    query = st.text_area("Your Question:", height=100)

    if st.button("Get Answer"):
        if not query:
            st.warning("Please enter a question")
        else:
            retriever = st.session_state.get("retriever")

            if not callable(retriever):
                st.error("❌ Retriever is not initialized correctly. Please scrape the website again.")
            else:
                with st.spinner("Analyzing content..."):
                    try:
                        # Retrieve relevant documents
                        docs = retriever(query)
                        
                        # Prepare context for RAG
                        context = "\n\n".join([doc.page_content for doc in docs])
                        
                        # Get RAG chain and invoke
                        rag_chain = get_rag_chain()
                        answer = rag_chain.invoke({
                            "context": context,
                            "question": query
                        })

                        st.subheader("Answer:")
                        st.markdown(answer)

                        with st.expander("View Source Context"):
                            for i, doc in enumerate(docs, 1):
                                st.markdown(f"**Source {i}:**")
                                st.text(doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else ""))
                    
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")