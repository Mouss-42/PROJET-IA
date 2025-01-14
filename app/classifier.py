import re
from unidecode import unidecode
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('french'))

def preprocess_text(text):
    text = unidecode(text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return ' '.join([lemmatizer.lemmatize(word) for word in words if word not in stop_words])

def get_ngrams(text, n):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

def keyword_match(keyword, text):
    keyword_parts = keyword.split()
    text_parts = text.split()
    return any(all(part in text_parts for part in keyword_parts[i:i+len(keyword_parts)]) for i in range(len(text_parts)))

class SISRSLAMClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=5000)
        self.classifier = MultinomialNB()
        self.trained = False

    def train(self, descriptions, labels):
        X = self.vectorizer.fit_transform(descriptions)
        self.classifier.fit(X, labels)
        self.trained = True

    def classify(self, description):
        if not self.trained:
            raise ValueError("Classifier not trained yet")
        
        preprocessed_description = preprocess_text(description)
        X = self.vectorizer.transform([preprocessed_description])
        probabilities = self.classifier.predict_proba(X)[0]
        
        sisr_score = probabilities[self.classifier.classes_ == 'SISR'][0] * 100
        slam_score = probabilities[self.classifier.classes_ == 'SLAM'][0] * 100

        if abs(sisr_score - slam_score) < 5:
            result = "Indécis"
        elif sisr_score > slam_score:
            result = "SISR"
        else:
            result = "SLAM"

        return result, sisr_score, slam_score

# Example usage
if __name__ == "__main__":
    # Training data
    descriptions = [
        "J'aime développer des applications et des sites web",
        "Je suis passionné par les réseaux et la sécurité informatique",
        "J'adore programmer en Python et Java",
        "Je m'intéresse à l'administration des systèmes et au cloud computing"
    ]
    labels = ["SLAM", "SISR", "SLAM", "SISR"]

    classifier = SISRSLAMClassifier()
    classifier.train(descriptions, labels)

    # Test the classifier
    description = input("Décrivez vos préférences : ")
    result, sisr_score, slam_score = classifier.classify(description)
    print(f"Orientation suggérée : {result}")
    print(f"Score SISR : {sisr_score:.2f}%")
    print(f"Score SLAM : {slam_score:.2f}%")