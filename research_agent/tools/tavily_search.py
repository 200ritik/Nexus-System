import os
import logging

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

from configuration.config import TAVILY_MAX_RESULTS
from research_agent.sources.trusted_sources import (
    OPEN_FDA_DRUG_LABEL_API,
    MEDLINEPLUS_API,
    WHO_HEALTH_TOPICS,
    NCDC_INDIA,
    PUBCHEM_API,
)

load_dotenv()
logger = logging.getLogger(__name__)

tavily_client = TavilyClient(
    api_key=os.environ["TAVILY_API_KEY"]
)

TRUSTED_DOMAINS = [
    "open.fda.gov",
    "api.fda.gov",
    "medlineplus.gov",
    "who.int",
    "ncdc.gov.in",
    "pubchem.ncbi.nlm.nih.gov",
]


@tool
def research_agent(query: str) -> list[dict]:
    """Search trusted sources for medical or medicine information."""

    response = tavily_client.search(
        query=query,
        max_results=TAVILY_MAX_RESULTS,
        search_depth="advanced",
        include_domains=TRUSTED_DOMAINS,
    )

    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
        }
        for item in response.get("results", [])
    ]