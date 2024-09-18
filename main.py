from fastapi import FastAPI, HTTPException, Depends, Request 
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from functools import lru_cache
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from config import Settings
from scraper import scrape_website
from fastapi import Request, Depends, HTTPException, Query



app = FastAPI()

#
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ScrapeRequest(BaseModel):
    url: str

@lru_cache()
def get_settings():
    return Settings()



@app.post("/scrape")
async def scrape_endpoint(
    request: Request, 
    url: str = Query(..., description="The URL to scrape"), 
    settings: Settings = Depends(get_settings)
):
    print(f"Received scrape request for URL: {url}")
    try:
        result = await scrape_website(url, settings)
        print(f"Scraping completed. Extracted info: {result}")
        return {"extracted_info": result}
    except Exception as e:
        print(f"Error in scrape_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))