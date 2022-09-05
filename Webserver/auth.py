from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from Database.db import database

da = database()

X_API_KEY = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def apikey(X_API_KEY: str = Security(X_API_KEY)):
    if da.login_check(X_API_KEY):
        return X_API_KEY
    else:
        raise HTTPException(
            status_code=403,
            detail="Unable to Validate your API KEY, Try signing up",
        )
