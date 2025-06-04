from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
from bs4 import BeautifulSoup

load_dotenv()

mcp = FastMCP("docs")

USER_AGENT = "docs-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}

async def search_web(query: str) -> dict | None:
    print("Searching the web...")

def fetch_url():
    print("Fetching URL...")

@mcp.tool()
def get_docs():
    print("Getting docs...")


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()