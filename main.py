
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from functools import lru_cache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.calculations.config import Settings
from src.calculations.scraper import scrape_website
from fastapi import Query

# Initialize the FastAPI app
app = FastAPI()

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

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
@limiter.limit("5/minute")  # Set rate limit: 5 requests per minute
async def scrape_endpoint(
    request: Request,
    url: str = Query(..., description="The URL to scrape"),
    settings: Settings = Depends(get_settings),
):
    print(f"Received scrape request for URL: {url}")
    try:
        result = await scrape_website(url, settings)
        print(f"Scraping completed. Extracted info: {result}")
        return {"extracted_info": result}
    except Exception as e:
        print(f"Error in scrape_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)