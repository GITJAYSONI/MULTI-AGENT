from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv 
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) 

@tool
def comprehensive_search(query : str) -> str:
    """Search the web and YouTube for recent and reliable information on a topic. Returns titles, URLs and snippets and youtube video links if available"""
    
    # 1. Fetch general web articles
    web_results = tavily.search(query=query, max_results=5)
    
    # 2. Fetch specific YouTube videos
    yt_results = tavily.search(query=query, search_depth="advanced", include_domains=["youtube.com"], max_results=3)

    out = []
    
    for r in web_results.get('results', []):
        out.append(f"Title: {r['title']} \nURL: {r['url']} \nSnippet: {r['content'][:300]} \n")

    
    for r in yt_results.get('results', []):
        out.append(f"Video Title: {r['title']} \nYouTube Link: {r['url']} \nDescription: {r['content'][:500]} \n")

    return "\n----\n".join(out)

print(comprehensive_search.invoke("What is the latest news about gold?"))

