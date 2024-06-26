import json

import requests

# Replace these with your own API key and video ID
API_KEY = "AIzaSyD1SVPtYRn38EzN-OXcShuVoV7McWUWfrw"
VIDEO_ID = "M2_wEDek554"
COMMENTS_FILE = "comments.json"

# Define the base API URLs
base_comment_threads_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId={VIDEO_ID}&key={API_KEY}&maxResults=100"
base_comments_url = (
    f"https://www.googleapis.com/youtube/v3/comments?part=snippet&key={API_KEY}"
)


# Function to fetch comments from YouTube API
def fetch_comments(api_url):
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
                # Fetch replies if any
                if "replies" in item:
                    for reply in item["replies"]["comments"]:
                        reply_text = reply["snippet"]["textOriginal"]
                        comments.append(reply_text)

                # If more than 5 replies, fetch the rest using the comments endpoint
                total_reply_count = item["snippet"]["totalReplyCount"]
                if total_reply_count > 5:
                    parent_id = item["id"]
                    comments.extend(fetch_all_replies(parent_id))

            api_url = data.get("nextPageToken")
            if api_url:
                api_url = f"{base_comment_threads_url}&pageToken={api_url}"
            else:
                break
        else:
            print(f"Failed to fetch comments: {response.status_code}")
            break

    return comments


# Function to fetch all replies for a given parent comment
def fetch_all_replies(parent_id):
    replies = []
    api_url = f"{base_comments_url}&parentId={parent_id}&maxResults=100"
    while api_url:
        response = requests.get(api_url)
        print(f"Request URL (replies): {api_url}")
        print(f"Request status (replies): {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            items_count = len(data.get("items", []))
            print(f"Fetched {items_count} replies")

            for item in data.get("items", []):
                reply_text = item["snippet"]["textOriginal"]
                replies.append(reply_text)

            api_url = data.get("nextPageToken")
            if api_url:
                api_url = (
                    f"{base_comments_url}&parentId={parent_id}&pageToken={api_url}"
                )
            else:
                break
        else:
            print(f"Failed to fetch replies: {response.status_code}")
            break

    return replies


# Fetch comments
comments = fetch_comments(base_comment_threads_url)

# Save comments to a JSON file
with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
    json.dump(comments, f, ensure_ascii=False, indent=4)

print(f"Saved {len(comments)} comments to {COMMENTS_FILE}")
