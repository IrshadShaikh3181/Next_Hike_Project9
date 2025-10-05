"""
Setup Guide for News Research Tool
Run this script to verify your setup and test API connections
"""

import os
import requests
from newsapi import NewsApiClient

def test_newsapi_connection(api_key):
    """Test NewsAPI connection"""
    print("Testing NewsAPI connection...")
    try:
        newsapi = NewsApiClient(api_key=api_key)
        # Test with a simple query
        articles = newsapi.get_everything(q='python', page_size=1)
        if articles['status'] == 'ok':
            print("✅ NewsAPI connection successful!")
            print(f"Total articles available: {articles['totalResults']}")
            return True
        else:
            print("❌ NewsAPI connection failed!")
            return False
    except Exception as e:
        print(f"❌ NewsAPI error: {e}")
        return False

def test_groq_connection(api_key):
    """Test Groq API connection"""
    print("Testing Groq API connection...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": "Hello, this is a test."}],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print("✅ Groq API connection successful!")
            return True
        else:
            print(f"❌ Groq API failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return False

def main():
    """Main setup verification function"""
    print("=== News Research Tool Setup Verification ===\n")
    
    # Check for API keys
    newsapi_key = os.getenv('NEWSAPI_KEY')
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not newsapi_key:
        newsapi_key = input("Enter your NewsAPI key: ").strip()
    
    if not groq_key:
        groq_key = input("Enter your Groq API key: ").strip()
    
    if not newsapi_key or not groq_key:
        print("❌ Both API keys are required!")
        return
    
    print("\n1. Testing API Connections:")
    print("-" * 30)
    
    newsapi_success = test_newsapi_connection(newsapi_key)
    groq_success = test_groq_connection(groq_key)
    
    print(f"\n2. Setup Summary:")
    print("-" * 30)
    print(f"NewsAPI: {'✅ Working' if newsapi_success else '❌ Failed'}")
    print(f"Groq API: {'✅ Working' if groq_success else '❌ Failed'}")
    
    if newsapi_success and groq_success:
        print("\n🎉 Setup complete! You can now run the application:")
        print("streamlit run app.py")
    else:
        print("\n❌ Setup incomplete. Please check your API keys and try again.")
        print("\nTroubleshooting:")
        if not newsapi_success:
            print("- Verify your NewsAPI key at https://newsapi.org/account")
        if not groq_success:
            print("- Verify your Groq API key at https://console.groq.com/keys")

if __name__ == "__main__":
    main()