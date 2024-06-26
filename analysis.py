import json
from collections import defaultdict

import nltk
from textblob import TextBlob

# Download the necessary NLTK data
nltk.download("punkt")

# Load comments from the JSON file
with open("comments.json", "r") as file:
    comments = json.load(file)

# Names to check
people = ["Bardella", "Attal", "Bompard"]

# Initialize counters for each person
sentiment_counts = {
    person: {"positive": 0, "negative": 0, "total": 0} for person in people
}


# Function to determine sentiment
def get_sentiment(text):
    blob = TextBlob(text)
    return "positive" if blob.sentiment.polarity >= 0 else "negative"


# Analyze each comment
for comment in comments:
    for person in people:
        if person.lower() in comment.lower():
            sentiment = get_sentiment(comment)
            sentiment_counts[person][sentiment] += 1
            sentiment_counts[person]["total"] += 1
            break  # Only count the comment for the first person found

# Calculate percentages
percentages = {}
for person, counts in sentiment_counts.items():
    total = counts["total"]
    if total > 0:
        positive_percentage = (counts["positive"] / total) * 100
        negative_percentage = (counts["negative"] / total) * 100
        percentages[person] = {
            "positive_percentage": positive_percentage,
            "negative_percentage": negative_percentage,
        }

# Display the results
import pprint

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(percentages)
