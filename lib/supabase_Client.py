import os
from dotenv import load_dotenv
from supabase import create_client

# Load .env.local file
load_dotenv(dotenv_path=".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL and/or SUPABASE_KEY not found in .env.local")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
