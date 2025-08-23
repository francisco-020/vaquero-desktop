import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from supabase import create_client

# Resolve the env file reliably (project root /.env.local)
#    – works whether you run from PyCharm or `python -m my_app.main`
ROOT = Path(__file__).resolve().parents[1]  # -> <project-root>
ENV_PATH = ROOT / ".env.local"

# Optional: fall back to searching if you ever rename/move it
if not ENV_PATH.exists():
    found = find_dotenv(".env.local", usecwd=True)
    ENV_PATH = Path(found) if found else ENV_PATH

# Load .env.local file
loaded = load_dotenv(dotenv_path=ENV_PATH, override=False)

SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL and/or SUPABASE_KEY not found in .env.local")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
