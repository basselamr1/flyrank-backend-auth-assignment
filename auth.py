from supabase_client import supabase
from fastapi import HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

        user = response.user

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return user

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or expired token"}
        )