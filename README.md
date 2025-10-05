🧠 LLM Project: Building a News Research Tool

This project builds a **News Research Tool** using **LangChain**, **OpenAI API**, and **Streamlit**.  
It allows users to enter a query and receive summarized, relevant news articles — designed especially for **equity research analysts** and **data enthusiasts**.

---

## 📋 Project Overview

The goal of this project is to:
- Fetch real-time news articles from **NewsAPI**.
- Use **LangChain + OpenAI LLMs** to summarize the results.
- Display insights in an interactive **Streamlit** interface.

---

## 🧱 Project Structure

```
├── app.py                  # Streamlit web app
├── langchain_config.py     # LangChain + API configuration
├── .env                    # Stores your API keys (not committed)
├── .env.example            # Example for others
├── .gitignore              # Ignores environment files
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

---

## ⚙️ Phase 1: Environment Setup

### 1️⃣ Install Required Libraries
```bash
pip install langchain openai streamlit newsapi-python python-dotenv
```

### 2️⃣ Get API Keys
- **OpenAI API key** → [https://platform.openai.com](https://platform.openai.com)  
- **NewsAPI key** → [https://newsapi.org](https://newsapi.org)

Store both keys securely in a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
NEWSAPI_KEY=your_newsapi_key
```

---

## 🧩 Phase 2: LangChain Configuration

Create `langchain_config.py`:

```python
import os
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from newsapi import NewsApiClient

load_dotenv()

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
newsapi_key = os.getenv("NEWSAPI_KEY")

# Initialize clients
openai = OpenAI(api_key=openai_api_key)
newsapi = NewsApiClient(api_key=newsapi_key)

# Functions to fetch and summarize news
def get_news_articles(query):
    articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
    return articles['articles']

def summarize_articles(articles):
    summaries = [a['description'] for a in articles if a['description']]
    return ' '.join(summaries)

def get_summary(query):
    articles = get_news_articles(query)
    return summarize_articles(articles)

template = """
You are an AI assistant helping an equity research analyst.
Given the following query and news summaries, provide a concise analysis.

Query: {query}
Summaries: {summaries}
"""

prompt = PromptTemplate(template=template, input_variables=['query', 'summaries'])
llm_chain = LLMChain(prompt=prompt, llm=openai)
```

---

## 💻 Phase 3: Streamlit Interface

Create `app.py`:

```python
import streamlit as st
from langchain_config import llm_chain, get_summary

st.title('📰 Equity Research News Tool')
st.write('Enter your query to get summarized insights from recent news.')

query = st.text_input('Enter your query:')

if st.button('Get News'):
    if query:
        summaries = get_summary(query)
        response = llm_chain.run({'query': query, 'summaries': summaries})
        st.subheader('📊 Summary:')
        st.write(response)
    else:
        st.warning('Please enter a query.')
```

Run the app:
```bash
streamlit run app.py
```

---

## 🧪 Phase 5: Testing & Validation

✅ Verify:
- App runs without errors.  
- Entering a query returns summarized news articles.  
- The summaries are accurate and relevant.  

---

## 📘 Phase 6: Documentation & Finalization

- Documented all functions and steps.  
- Ensure dependencies are listed in `requirements.txt`:  
  ```
  langchain
  openai
  streamlit
  newsapi-python
  python-dotenv
  ```
- Clean up unused code before deployment.

---

## 🌟 Optional Enhancements
- 🔐 Add user authentication.
- 🎨 Improve UI/UX with Streamlit components.
- 📊 Add query history or export results.

---

## 🚀 Run the Project

```bash
# Step 1: Clone repo
git clone <your_repo_url>
cd <repo_name>

# Step 2: Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Add your .env file
# Step 5: Run the app
streamlit run app.py
```

---

## 🧑‍💻 Author

**Name:** [Irshad Shaikh](https://github.com/irshadshaikh)  
**Project by:** *Nexthikes LLM Course Team*  

