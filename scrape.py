from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
AUTH = 'brd-customer-hl_c8857878-zone-naviqa:vjkpak4icce5'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'


def scrape_website(website):
    print("Launching chrome browser... ")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
def extract_body_content(html_content):
    soup=BeautifulSoup(html_content, "html.parser")
    body_content=soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup=BeautifulSoup(body_content,"html.parser")
    for script_or_style in soup(["script","style"]):
        script_or_style.extract()

    cleaned_content=soup.get_text(separator="\n")
    cleaned_content="\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i+max_length] for i in range(0,len(dom_content),max_length)
    ]

def store_in_chromadb(cleaned_content):
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(cleaned_content)
    
    # Store in ChromaDB
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory="./scraped_website_db"  # New folder for scraped data
    )
    return vector_store.as_retriever()