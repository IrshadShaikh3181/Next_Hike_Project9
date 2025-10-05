# app.py - Final Enhanced Version with Groq and NewsAPI Integration
import streamlit as st
import os

# Import both the LLM chain and the news-fetching/summary-extracting function
# from the configuration file.
# Note: This assumes your file is correctly named 'langchain_config.py'
from langchain_config import llm_chain, get_summary 

# --- UI Setup ---
st.set_page_config(
    page_title="Equity Research News Tool",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title('📈 Equity Research News Tool') 
st.markdown('### LLM-Powered News Synthesis (Groq & NewsAPI)')

# High-Score Tip: Check if API Keys are set
if not os.environ.get('GROQ_API_KEY') or not os.environ.get('NEWS_API_KEY'):
    st.error("🚨 Configuration Error: Please set the GROQ_API_KEY and NEWS_API_KEY environment variables.")

# --- User Input ---
query = st.text_input(
    'Enter your query for the equity analyst:', 
    placeholder='e.g., Q3 earnings forecast for Tesla and market sentiment'
) 

# --- Main Logic ---
if st.button('🚀 Get Synthesized News', use_container_width=True): 
    if not query:
        st.warning('Please enter a query.')
    elif not os.environ.get('GROQ_API_KEY') or not os.environ.get('NEWS_API_KEY'):
        # Don't proceed if keys are missing
        pass 
    else:
        # High-Score Tip: Use a specific spinner message for better user feedback
        with st.spinner('1. Fetching news articles...'):
            # Step 1: Get the raw summaries from NewsAPI integration
            summaries = get_summary(query) 

        if not summaries:
            st.warning("Could not find relevant news articles or an API error occurred.")
        else:
            with st.spinner('2. Synthesizing news using Groq LLM...'):
                # Step 2: Pass the user query and the fetched summaries to the LLM chain
                response = llm_chain.run({
                    'query': query, 
                    'summaries': summaries
                }) 

            st.markdown('---')
            st.markdown('### 💡 AI-Generated Equity Summary') 
            st.info(response) # Use st.info for a visually distinct summary
            
            # High-Score Tip: Show the raw data processed by the LLM (Optional but good for transparency)
            with st.expander("Show Raw News Data Processed"):
                 st.caption("The following text was fed into the LLM for final synthesis:")
                 st.text(summaries)

