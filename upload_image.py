# upload_image.py
from lib.supabase_Client import SUPABASE_URL
import requests

def upload_file_to_storage(file_path, file_name, access_token):
    """Uploads file to Supabase 'listings' bucket using user access token and returns public URL."""
    with open(file_path, "rb") as file:
        file_data = file.read()

    upload_url = f"{SUPABASE_URL}/storage/v1/object/listings/{file_name}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
    }

    response = requests.post(upload_url, headers=headers, data=file_data)

    if response.ok:
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/listings/{file_name}"
        print("Uploaded successfully:", public_url)
        return public_url
    else:
        print("Upload failed:", response.status_code, response.text)
        return None
