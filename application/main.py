"""main.py
Python FastAPI Auth0 integration example
"""
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()
# Creates app instance
app = FastAPI()


@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result


@app.get("/api/private")
def private(token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""

    result = token.credentials

    return result
