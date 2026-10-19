from langchain.tools import tool

from research_agent.tools.tavily_search import research_agent
from research_agent.tools.data_scraping import scrape_url


@tool
def medical_research(query: str) -> dict:
    """Search and extract relevant medical information."""

    search_results = research_agent.invoke(
        {"query": query}
    )

    pages = []

    for result in search_results[:3]:
        url = result.get("url")

        if not url:
            continue

        content = scrape_url.invoke({"url": url})

        pages.append({
            "title": result.get("title"),
            "url": url,
            "content": content,
        })

    return {
        "query": query,
        "sources": pages,
    }