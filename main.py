from auth import get_current_user
from supabase_client import supabase
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel

app = FastAPI()

class AuthRequest(BaseModel):
    email: str | None = None
    password: str | None = None

@app.get('/')
async def root():
    return {"message": "Server running and connected to Supabase."}

@app.post('/auth/signup', status_code=status.HTTP_201_CREATED)
async def signup(request: AuthRequest):
    if request.email is None or request.password is None: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Missing email or password."
        )
    try:
        response = supabase.auth.sign_up(
            {
                "email": request.email,
                "password": request.password
            }
        )
        return response.user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post('/auth/login', status_code= status.HTTP_200_OK)
async def login(request: AuthRequest):
    if request.email is None or request.password is None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Email or password is missing."
        )
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": request.email,
                "password": request.password
            }
        )
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": str(e)}
        )

@app.get('/public/info', status_code= status.HTTP_200_OK)
async def get_public_info():
    return {"message": "Welcome stranger! This info is public."}
    
@app.get('/protected/profile')
async def get_protected_profile(user = Depends(get_current_user)):
    return user

@app.post('/auth/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    supabase.auth.sign_out()