import os
import requests
from dotenv import load_dotenv

load_dotenv('./.env')

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"] 
USER_ID = os.environ["USER_ID"] 
MEDIA_ENDPOINT = f"https://graph.instagram.com/v12.0/{USER_ID}/media"


def fetch_media(url=None):
    """
    Fetch media metadata from the Instagram API, handling pagination.
    """
    media = []
    next_url = url or MEDIA_ENDPOINT

    while next_url:
        print(f"Fetching media from: {next_url}")
        params = {
            "fields": "id,media_type,media_url,caption,timestamp,children",
            "access_token": ACCESS_TOKEN,
        }
        response = requests.get(next_url, params=None if url else params)
        
        if response.status_code == 200:
            data = response.json()
            media.extend(data.get("data", []))
            next_url = data.get("paging", {}).get("next")  # Get the next page URL
        else:
            print("Error fetching media:", response.json())
            break

    return media


def fetch_carousel_children(media_id):
    """
    Fetch all child media for a carousel album.
    """
    endpoint = f"https://graph.instagram.com/{media_id}/children"
    params = {
        "fields": "id,media_type,media_url",
        "access_token": ACCESS_TOKEN,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error fetching carousel children for {media_id}:", response.json())
        return []


def download_file(url, file_path):
    """
    Download a file from a URL and save it to the specified path.
    """
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded: {file_path}")


def media_exists(file_path):
    """
    Check if a media file already exists in the folder.
    """
    return os.path.exists(file_path)


def download_media(media_data):
    """
    Download all media (images, videos, and carousel items) to local storage.
    If a media file already exists, skip downloading it.
    """
    os.makedirs("instagram_media", exist_ok=True)

    for media in media_data:
        media_type = media.get("media_type")
        media_url = media.get("media_url")
        media_id = media.get("id")

        if media_type in ["IMAGE", "VIDEO"]:
            file_extension = "mp4" if media_type == "VIDEO" else "jpg"
            file_path = f"instagram_media/{media_id}.{file_extension}"

            if media_exists(file_path):
                print(f"File already exists, skipping: {file_path}")
                continue

            print(f"Downloading {media_type.lower()}: {media_id}")
            download_file(media_url, file_path)

        elif media_type == "CAROUSEL_ALBUM":
            print(f"Handling carousel album: {media_id}")
            children = fetch_carousel_children(media_id)

            for child in children:
                child_type = child.get("media_type")
                child_url = child.get("media_url")
                child_id = child.get("id")
                file_extension = "mp4" if child_type == "VIDEO" else "jpg"
                file_path = f"instagram_media/{child_id}.{file_extension}"

                if media_exists(file_path):
                    print(f"File already exists, skipping: {file_path}")
                    continue

                print(f"  Downloading {child_type.lower()} from carousel: {child_id}")
                download_file(child_url, file_path)


def main():
    try:
        print("Fetching all media...")
        media_data = fetch_media()
        
        if media_data:
            print(f"Found {len(media_data)} media items. Starting download...")
            download_media(media_data)
        else:
            print("No media found.")
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        print("Continuing with remaining media...")

if __name__ == "__main__":
    main()
