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




app = FastAPI()

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

class ScrapeRequest(BaseModel):
    url: str

@lru_cache()
def get_settings():
    return Settings()

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Try again later."},
    )

@app.post("/scrape")
@limiter.limit("5/minute")
async def scrape_endpoint(request : Request, settings: Settings = Depends(get_settings)):
    try:
        result = await scrape_website(request.url, settings)
        return {"extracted_info": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)