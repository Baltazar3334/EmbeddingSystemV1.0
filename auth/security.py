"""
API token authentication.
"""

import os

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# BEARER SCHEME
security = HTTPBearer()


# SECRET TOKEN
API_SECRET = os.getenv("API_SECRET")

if not API_SECRET:
    raise RuntimeError(
        "API_SECRET not configured. Check if you have .env file."
    )


# VERIFY TOKEN
def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):

    token = credentials.credentials

    if token != API_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Invalid API token"
        )

    return token