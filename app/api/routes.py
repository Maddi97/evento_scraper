from fastapi import APIRouter, HTTPException
from app.models.request_models import UrlsRequest
from app.services.scraper import scrape_multiple_urls

router = APIRouter()

@router.post("/scrapeEventsFromUrls")
async def scrape(request: UrlsRequest):
    try:
        results = await scrape_multiple_urls(request.urls)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
