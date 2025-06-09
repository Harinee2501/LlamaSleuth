import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, store_in_chromadb
from parse import get_rag_chain
import sys
import asyncio
import torch

# Configuration
st.set_page_config(layout="wide")
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Display hardware info
st.sidebar.markdown(f"**Running on:** {'GPU 🚀' if torch.cuda.is_available() else 'CPU ⚙️'}")

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
            retriever_fn = st.session_state.get("retriever")

            if not callable(retriever_fn):
                st.error("❌ Retriever is not initialized correctly. Please scrape the website again.")
            else:
                with st.spinner("Analyzing content..."):
                    try:
                        # Call retriever - now returns (results, debug_data)
                        results, debug_data = retriever_fn(query)

                        # Retrieval diagnostics
                        with st.expander("🔍 Retrieval Diagnostics"):
                            tab1, tab2, tab3 = st.tabs(["Vector Results", "Keyword Results", "Final Ranking"])

                            with tab1:
                                st.write("Semantic Search Results:")
                                st.json(debug_data.get("vector_results", []))

                            with tab2:
                                st.write("Keyword Match Results:")
                                st.json(debug_data.get("keyword_results", []))

                            with tab3:
                                st.write("Reranked Results (BERT Score):")
                                for i, (doc, score) in enumerate(zip(debug_data.get("reranked_results", []),
                                                                 debug_data.get("scores", []))):
                                    st.markdown(f"**#{i+1}** (Score: {score:.2f}):")
                                    st.text(doc[:500] + ("..." if len(doc) > 500 else ""))

                        # Final answer
                        rag_chain = get_rag_chain()
                        answer = rag_chain.invoke({
                            "context": "\n\n".join([doc.page_content for doc in results]),
                            "question": query
                        })

                        st.subheader("Answer:")
                        st.markdown(answer)

                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")