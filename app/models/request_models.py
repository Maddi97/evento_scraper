from pydantic import BaseModel, HttpUrl
from typing import List

class UrlsRequest(BaseModel):
    urls: List[HttpUrl]
