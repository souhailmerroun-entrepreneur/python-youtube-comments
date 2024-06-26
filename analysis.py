import json
from collections import defaultdict

import nltk
from transformers import pipeline

# Download the necessary NLTK data
nltk.download("punkt")

# Load comments from the JSON file
with open("comments.json", "r") as file:
    comments = json.load(file)

# Names to check and their variations
people = {
    "Bardella": ["Bardella", "Jordan", "RN", "marine"],
    "Attal": ["Attal", "Gabriel", "Renaissance"],
    "Bompard": ["Bompard", "Manuel", "NFP", "Front Populaire", "Nouveau"]
}

# Initialize counters for each person
sentiment_counts = {
    person: {"positive": 0, "negative": 0, "total": 0} for person in people
}

# Initialize the sentiment analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Function to determine sentiment
def get_sentiment(text):
    result = sentiment_analysis(text)[0]
    sentiment = result['label']
    # Convert the label to positive or negative
    return "positive" if sentiment in ["4 stars", "5 stars"] else "negative"

# Analyze each comment
for comment in comments:
    found_people = set()
    for person, variations in people.items():
        for variation in variations:
            if variation.lower() in comment.lower():
                found_people.add(person)
                break
    
    if found_people:
        sentiment = get_sentiment(comment)
        print(f"Comment: {comment}")
        for person in found_people:
            sentiment_counts[person][sentiment] += 1
            sentiment_counts[person]["total"] += 1
            print(f"Person: {person}\nSentiment: {sentiment}")
        print("-" * 50)  # Separator for clarity
    else:
        print(f"Comment: {comment}\nPerson: None\nSentiment: Not Analyzed")
        print("-" * 50)  # Separator for clarity

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
