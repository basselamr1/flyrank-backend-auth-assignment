from supabase_client import supabase
from fastapi import Header
from fastapi.responses import JSONResponse

async def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization :
        return JSONResponse(
            status_code= 401,
            content = {"error": "Access token required"}
        )
    parts = authorization.split()

    if len(parts)!=2 or parts[0].lower()!="bearer" or not parts[1]:
        return JSONResponse(
            status_code= 401,
            content = {"error": "Access token required"}
        )
    
    token = parts[1]

    try:
        response = supabase.auth.get_user(token)
        user = response.user
        if user is None:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid or expired token"}
            )
        return user

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or expired token"}
        )