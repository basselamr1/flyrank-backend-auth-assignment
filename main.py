import os 
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException, status, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv(override = True)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
PORT = int(os.getenv("PORT"))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
            detail={"error": "Invalid login credentials"}
        )

@app.get('/public/info', status_code= status.HTTP_200_OK)
async def get_public_info():
    return {"message": "Welcome stranger! This info is public."}
    
@app.get('/protected/profile')
async def get_protected_profile(authorization: str | None = Header(default =  None)):
    
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
    return token