"""main.py
Python FastAPI Auth0 integration example
"""
from fastapi import Depends, FastAPI, Response, status
from fastapi.security import HTTPBearer
import requests
from .utils import VerifyToken # pylint: disable=E0402

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
def private(response: Response, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""

    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return result


@app.get("/api/private/profile")
def private_profile(response: Response, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route
    """
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    headers = {'authorization': f"Bearer {token.credentials}"}
    url_items = "https:// your.domain.auth0.com/userinfo"
    profile = requests.get(
        url_items,
        headers=headers,
        timeout=(2.0, 3.5)
    )

    return profile.json()
