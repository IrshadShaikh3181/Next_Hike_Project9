# langchain_config.py - TEMPORARY HARDCODED KEYS FOR TROUBLESHOOTING

import os
from newsapi import NewsApiClient
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core._api.deprecation import surface_langchain_deprecation_warnings

# =========================================================================
# !!! WARNING !!!
# This method is ONLY for troubleshooting environment issues. 
# For your final submission, you MUST return to using the .env file 
# and os.environ.get('KEY_NAME') for a high grade.
# =========================================================================

# --- 1. Set Your VALID API Keys Here ---
# Paste your actual keys inside the quotes.
# This bypasses the os.environ.get and .env file loading entirely.

NEWS_API_KEY_MANUAL = "b0e757f75f8f469f86da3509cb74da8b"  
GROQ_API_KEY_MANUAL = "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"

# --- 2. Groq LLM Setup ---
# Initialize Groq LLM using the key directly.
llm = ChatGroq(
    temperature=0, 
    model_name="llama3-8b-8192",
    api_key=GROQ_API_KEY_MANUAL # Passing the key directly to the model constructor
) 

# --- 3. NewsAPI Setup ---
# Initialize NewsAPI Client using the key directly.
newsapi = NewsApiClient(api_key=NEWS_API_KEY_MANUAL) 

# --- 4. Core Functions (No change from before) ---

def get_news_articles(query):
    """Fetches news articles for a given query."""
    try:
        articles = newsapi.get_everything(
            q=query, 
            language='en',
            sort_by='relevancy',
            page_size=10
        )
        # Note: If NewsAPI fails, it will still throw an error code here.
        return articles.get('articles', [])
    except Exception as e:
        # If we reach here, it's definitely a key or rate limit issue.
        print(f"NewsAPI Error during fetch (Manual Test): {e}")
        return []

def summarize_articles(articles):
    """Extracts and concatenates the description (summary) from each article."""
    summaries = [article['description'] for article in articles if article.get('description')]
    return ' '.join(summaries)

def get_summary(query):
    """Primary function to fetch news and extract summaries."""
    articles = get_news_articles(query)
    
    if not articles:
        # If we get no articles, return a message to the app
        return "No articles found."
        
    summary = summarize_articles(articles)
    return summary

# --- 5. Define the Prompt Template and LLM Chain ---

template = """
You are an AI assistant helping an equity research analyst. Your primary goal is to synthesize information accurately and quickly.
Given the following query and the provided news article summaries, provide an overall, concise summary that is highly relevant to an equity analyst.

Query: {query}
Summaries: {summaries}

###
"""

prompt = PromptTemplate(
    template=template,
    input_variables=['query', 'summaries']
)

llm_chain = LLMChain(prompt=prompt, llm=llm)
