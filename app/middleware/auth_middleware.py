from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import os
import requests
from jose import jwt, jwk
from jose.utils import base64url_decode

JWK = Dict[str, str]
JWKS = Dict[str, List[JWK]]

def get_jwks() -> JWKS:
    return requests.get(
        f"https://cognito-idp.{os.environ.get('AWS_REGION')}.amazonaws.com/{os.environ.get('COGNITO_USER_POOL_ID')}/.well-known/jwks.json"
    ).json()

def get_hmac_key(token: str, jwks: JWKS) -> Optional[JWK]:
    kid = jwt.get_unverified_header(token).get("kid")
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key

def verify_jwt(token: str, jwks: JWKS) -> bool:
    hmac_key = get_hmac_key(token, jwks)

    if not hmac_key:
        raise ValueError("No public key found!")

    hmac_key = jwk.construct(get_hmac_key(token, jwks))

    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode())

    return hmac_key.verify(message.encode(), decoded_signature)

class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        if request.url.path in ["/auth/login", "/auth/signup"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        if not token:
            return JSONResponse(status_code=401, content={"detail": "Invalid authentication token"})

        try:
            jwks = get_jwks()
            if verify_jwt(token, jwks):
                # You might want to decode the token and set user information in request.state here
                # For example:
                # payload = jwt.decode(token, jwks, algorithms=["RS256"])
                # request.state.user = payload
                pass
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
        except ValueError as ve:
            return JSONResponse(status_code=401, content={"detail": str(ve)})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})

        return await call_next(request)