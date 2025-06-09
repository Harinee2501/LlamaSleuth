from rank_bm25 import BM25Okapi
import numpy as np
from sentence_transformers import CrossEncoder
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from hashlib import md5
from langchain_core.documents import Document

# Bright Data configuration
AUTH = 'brd-customer-hl_69af7f50-zone-scraping_browser1:fscae93ekal6'
SBR_WS_CDP = f'wss://{AUTH}@brd.superproxy.io:9222'

async def scrape_website_async(website):
    print("Launching browser with Bright Data proxy...")
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
        try:
            page = await browser.new_page()
            print(f'Connected! Navigating to {website}')
            await page.goto(website, timeout=120000)
            print('Taking page screenshot to file page.png')
            await page.screenshot(path='./page.png', full_page=True)
            print('Navigated! Scraping page content...')
            html = await page.content()
            return html
        except Exception as e:
            print(f"Scraping failed: {str(e)}")
            raise
        finally:
            await browser.close()

def scrape_website(website):
    return asyncio.run(scrape_website_async(website))

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def create_hybrid_retriever(chunks, vector_retriever):
    tokenized_corpus = [doc.split() for doc in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def hybrid_retrieve(query, k=3):
        # Vector Search
        vector_results = vector_retriever.get_relevant_documents(query)
        
        # Keyword Search
        tokenized_query = query.split()
        bm25_scores = bm25.get_scores(tokenized_query)
        top_keyword_indices = np.argsort(bm25_scores)[-k*2:]
        keyword_docs = [Document(page_content=chunks[i]) for i in top_keyword_indices]
        
        # Deduplicate
        seen_contents = set()
        all_results = []
        for doc in vector_results + keyword_docs:
            content_hash = md5(doc.page_content.encode()).hexdigest()
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                all_results.append(doc)

        # Rerank
        pairs = [[query, doc.page_content] for doc in all_results]
        rerank_scores = reranker.predict(pairs)

        sorted_results = [doc for _, doc in sorted(zip(rerank_scores, all_results), reverse=True)]
        return sorted_results[:k]

    return hybrid_retrieve

def store_in_chromadb(cleaned_content, url):
    # Create unique collection name based on URL
    url_hash = md5(url.encode()).hexdigest()[:12]

    # Initialize Chroma client
    client = chromadb.PersistentClient(path="./scraped_website_db")

    # Check if collection exists before trying to delete
    existing_collections = [col.name for col in client.list_collections()]
    if url_hash in existing_collections:
        client.delete_collection(url_hash)

    # Split content into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(cleaned_content)

    if not chunks:
        return None

    # Create new collection with the content
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory="./scraped_website_db",
        collection_name=url_hash,
        client=client
    )

    vector_retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    return create_hybrid_retriever(chunks, vector_retriever)