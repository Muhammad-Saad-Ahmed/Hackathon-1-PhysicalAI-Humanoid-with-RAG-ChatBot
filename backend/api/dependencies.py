from fastapi import Header, HTTPException
from ..config.settings import settings


async def get_api_key(x_api_key: str = Header(...)):
    """
    Dependency to validate the X-API-KEY header for admin access.
    """
    if settings.ADMIN_API_KEY is None:
        # If ADMIN_API_KEY is not set in .env, allow access for development purposes
        return x_api_key
    
    if x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
