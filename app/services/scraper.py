import httpx
from typing import List, Dict
import asyncio
from bs4 import BeautifulSoup
from scraper import fetch_html, html_to_text, extract_body
from llm.langchain_parser import extract_event_data


async def scrape_multiple_urls(urls: List[str]) -> Dict[str, str]:
    results = {}

    async with httpx.AsyncClient() as client:
        tasks = [client.get(str(url), timeout=10.0) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for url, response in zip(urls, responses):
            if isinstance(response, Exception):
                results[str(url)] = f"Error: {str(response)}"
            else:
                try:

                    clean_body = extract_body.extract_relevant_body_content(response.text)
                    md = html_to_text.html_to_markdown(clean_body)
                    
                    ## not working
                    parsed = extract_event_data(md)

                    results[str(url)] = {
                        "extracted_event": parsed
                    }

                except Exception as parse_error:
                    results[str(url)] = f"Parsing error: {str(parse_error)}"

    return results