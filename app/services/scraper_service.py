from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Union
from app.models.event_models import EventSchema
import httpx
from typing import List, Dict
import asyncio
from app.core.scraper import html_to_text, extract_body
from app.core.scraper.scrape_with_js import scrape_with_js
from app.core.llm.langchain_parser import extract_event_data


class ScrapingException(Exception):
    pass


class ExtractedEventSuccess(BaseModel):
    type: Literal["success"]
    url: str
    extracted_event: EventSchema


class ExtractedEventError(BaseModel):
    type: Literal["error"]
    url: str
    error: str


ExtractedEvent = Union[ExtractedEventSuccess, ExtractedEventError]


async def scrape_multiple_urls(urls: List[HttpUrl]) -> List[ExtractedEvent]:
    results: List[ExtractedEvent] = []

    async with httpx.AsyncClient() as client:
        tasks = [client.get(str(url), timeout=10.0) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for url, response in zip(urls, responses):
            if isinstance(response, Exception):
                results.append(
                    ExtractedEventError(
                        type="error",
                        url=str(url),
                        error=f"Error {response}",
                    )
                )
            elif isinstance(response, httpx.Response):
                try:
                    text = response.text
                    if "Please enable JS" in text or "JavaScript is required" in text:
                        try:
                            text = await scrape_with_js(str(url))
                        except Exception as js_error:
                            results.append(
                                ExtractedEventError(
                                    type="error",
                                    url=str(url),
                                    error=f"JS-render failed: {str(js_error)}",
                                )
                            )

                    clean_body = extract_body.extract_relevant_body_content(text)
                    md = html_to_text.html_to_markdown(clean_body)
                    if len(md) < 50:
                        raise ScrapingException(f"Content too short for URL: {url}")

                    print("Continues to parse")
                    parsed = extract_event_data(md)
                    results.append(
                        ExtractedEventSuccess(
                            type="success", url=str(url), extracted_event=parsed
                        )
                    )
                except Exception as parse_error:
                    results.append(
                        ExtractedEventError(
                            type="error",
                            url=str(url),
                            error=f"Parse error: {str(parse_error)}",
                        )
                    )

    return results
