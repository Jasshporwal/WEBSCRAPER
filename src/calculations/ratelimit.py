from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


@limiter.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    response = await call_next(request)
    return response
