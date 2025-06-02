# 🔍 LlamaSleuth: AI-Powered Web Investigator

**Uncover hidden insights from any webpage using local AI and RAG technology.**  
*Detect scams, summarize content, and analyze data.*

---

## 🌟 Features
- **Local Web Scraping**: Selenium + ChromeDriver (no external APIs)
- **Smart Analysis**: RAG-powered with Ollama (Llama3) and ChromaDB
- **Offline-First**: Works without internet after initial setup
- **User-Friendly UI**: Streamlit dashboard for easy interaction

**Use Cases**:
- 🚨 Fake job/internship detection
- 📰 News/article summarization
- 🔍 Company/product research

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (match your Chrome version)
- [Ollama](https://ollama.ai) (for local LLMs)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LlamaSleuth.git
   cd NaviQA
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Download AI models:
   ```bash
  ollama pull llama3
  ollama pull mxbai-embed-large
  Place chromedriver.exe in project root
