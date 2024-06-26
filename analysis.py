import json
from collections import defaultdict

import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the sentiment intensity analyzer and spaCy NLP model
analyzer = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")


def analyze_comments(file_path):
    entity_sentiments = defaultdict(list)

    with open(file_path, "r", encoding="utf-8") as file:
        comments = json.load(file)

        for comment in comments:
            if comment:
                # Perform sentiment analysis
                sentiment = analyzer.polarity_scores(comment)
                sentiment_score = sentiment["compound"]

                # Perform entity recognition
                doc = nlp(comment)
                entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

                # Associate sentiment with entities
                for entity in entities:
                    entity_sentiments[entity].append(sentiment_score)

                # Print the comment, its sentiment score, and the identified entities
                print(f"Comment: {comment}")
                print(f"Sentiment Score: {sentiment_score}")
                print(f"Entities: {entities}\n")

    # Calculate the average sentiment score for each entity
    for entity, scores in entity_sentiments.items():
        average_sentiment = sum(scores) / len(scores) if scores else 0
        print(f"Entity: {entity}, Average Sentiment Score: {average_sentiment}")


# Example usage
file_path = "comments.json"  # Replace with the path to your JSON file
analyze_comments(file_path)
