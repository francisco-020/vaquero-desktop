# Initializing a connection to our Supabase backend
import os
from dotenv import load_dotenv
from supabase import create_client

# Load .env.local file
load_dotenv(dotenv_path=".env.local")

# assigning url link and key to SUPABASE_URL and SUPABASE_KEY
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Error handling if url or key are invalid
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL and/or SUPABASE_KEY not found in .env.local")

# assigning url and key using create_client function to variable named 
# "supabase" so we can import it in other files
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
