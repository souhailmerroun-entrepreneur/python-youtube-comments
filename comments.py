import json

import requests

# Replace these with your own API key and video ID
API_KEY = "AIzaSyD1SVPtYRn38EzN-OXcShuVoV7McWUWfrw"
VIDEO_ID = "Pqi3NNIdEaI"
COMMENTS_FILE = "comments.json"

# Define the base API URL
base_comment_threads_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={VIDEO_ID}&key={API_KEY}&maxResults=100"


# Function to fetch top-level comments from YouTube API
def fetch_top_comments(api_url):
    comments = []
    while api_url:
        response = requests.get(api_url)
        print(f"Request URL: {api_url}")
        print(f"Request status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            items_count = len(data.get("items", []))
            print(f"Fetched {items_count} comments")

            for item in data.get("items", []):
                top_comment = item["snippet"]["topLevelComment"]["snippet"][
                    "textOriginal"
                ]
                comments.append(top_comment)

            next_page_token = data.get("nextPageToken")
            if next_page_token:
                api_url = f"{base_comment_threads_url}&pageToken={next_page_token}"
            else:
                break
        else:
            print(f"Failed to fetch comments: {response.status_code}")
            break

    return comments


# Fetch top-level comments
top_comments = fetch_top_comments(base_comment_threads_url)

# Save top-level comments to a JSON file
with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
    json.dump(top_comments, f, ensure_ascii=False, indent=4)

print(f"Saved {len(top_comments)} top-level comments to {COMMENTS_FILE}")
