# LlamaSleuth: RAG- Powered Web Scraper

**Uncover hidden insights from any webpage using local AI and RAG technology.**  
*Detect scams, summarize content, and analyze data.*

---

## Features
- **Local Web Scraping**: Selenium + ChromeDriver (no external APIs)
- **Anti-Block Mechanism**: Bright Data integration for handling CAPTCHAs and IP rotation on protected sites
- **Smart Analysis**: RAG-powered with Ollama (Llama3) and ChromaDB
- **User-Friendly UI**: Streamlit dashboard for easy interaction

**Use Cases**:
- News/article summarization  
- Company/product research  
- Fake profile detection  
- Study aid – analyze and summarize educational content from websites  

---

## Installation

### Prerequisites
- Python 3.9+
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (match your Chrome version)
- [Ollama](https://ollama.ai) (for local LLMs)

### Steps
1. Clone the repository:
   ```bash 
   git clone https://github.com/yourusername/LlamaSleuth.git
   cd NaviQA
   ```
2. Install dependencies:
  ```bash  
   pip install -r requirements.txt
  ```
3. Download AI models:
  ```bash
   ollama pull llama3
   ollama pull mxbai-embed-large
  ```
4. Place chromedriver.exe in project root

---

## Quick Start

### Web Interface

```bash
streamlit run main.py
```

1. Enter a URL in the input box  
2. Click "Scrape Site"  
3. Ask questions about the content (e.g., *Is this job posting legitimate?*)

---

### Programmatic Use

```python
from scrape import scrape_website
from parse import analyze_content

content = scrape_website("https://example.com")
analysis = analyze_content(content, "Summarize key points")
print(analysis)
```


## Project Structure
```
NaviQA/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py                # Streamlit interface
├── scrape.py              # Web scraping logic
│   ├── scrape_website()
│   └── clean_content()
├── parse.py               # RAG processing
│   ├── analyze_content()
│   └── chunk_text()
└── chromedriver.exe       # Browser automation
```
     

## Tech Stack
![App Screenshot](tech.png)

## Troubleshooting

| Issue                 | Solution                                 |
|-----------------------|------------------------------------------|
| ChromeDriver error    | Download matching version from [here]([https://chromedriver.chromium.org/downloads](https://googlechromelabs.github.io/chrome-for-testing/#stable)) |
| Ollama model not found | Run `ollama pull llama3`                |
| Memory issues         | Reduce chunk size in `parse.py`         |


