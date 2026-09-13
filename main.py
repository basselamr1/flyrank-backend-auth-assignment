import os 
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import FastAPI

load_dotenv(override = True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PORT = int(os.getenv("PORT"))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")
    
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Server running and connected to Supabase."}