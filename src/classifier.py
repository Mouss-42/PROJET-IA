import re
from unidecode import unidecode
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

# Initialisation du lemmatiseur
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = unidecode(text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    # Lemmatisation des mots
    return ' '.join([lemmatizer.lemmatize(word) for word in words])

def get_ngrams(text, n):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

def keyword_match(keyword, text):
    keyword_parts = keyword.split()
    text_parts = text.split()
    return any(all(part in text_parts for part in keyword_parts[i:i+len(keyword_parts)]) for i in range(len(text_parts)))

def classify(description):
    # Poids ajustés des mots-clés
    sisr_keywords = {
        "serveur": 3, "virtualisation": 3, "réseau": 4, "sécurité": 3,  # Poids ajusté pour "réseau"
        "infrastructure": 2, "systeme": 2, "administration": 3, "cloud": 1.5,
        "firewall": 1.5, "vpn": 2, "maintenance": 1, "supervision": 1, "support": 1,
        "cisco": 2, "windows server": 2, "linux": 2, "active directory": 3
    }
    slam_keywords = {
        "application": 3, "base de données": 3, "développement": 3, "site web": 3,
        "programmation": 2, "logiciel": 2, "interface": 2, "dev": 3, "mobile": 2,
        "api": 1.5, "framework": 1.5, "algorithmique": 2, "objet": 1, "agile": 1,
        "full stack": 2, "front-end": 2, "back-end": 2, "java": 2, "python": 2,
        "javascript": 2, "php": 2, "c#": 2, "html": 1.5, "css": 1.5, "react": 2,
        "angular": 1.5, "vue": 1.5, "développer": 3, "coder": 3, "programmer": 3
    }

    preprocessed_description = preprocess_text(description)
    ngrams = get_ngrams(preprocessed_description, 3) + get_ngrams(preprocessed_description, 2) + preprocessed_description.split()

    sisr_score = sum(weight for keyword, weight in sisr_keywords.items() 
                     if any(keyword_match(preprocess_text(keyword), ngram) for ngram in ngrams))
    slam_score = sum(weight for keyword, weight in slam_keywords.items() 
                     if any(keyword_match(preprocess_text(keyword), ngram) for ngram in ngrams))

    total_weight = sum(sisr_keywords.values()) + sum(slam_keywords.values())
    sisr_score = (sisr_score / total_weight) * 100
    slam_score = (slam_score / total_weight) * 100

    if abs(sisr_score - slam_score) < 5:
        result = "Indécis"
    elif sisr_score > slam_score:
        result = "SISR"
    else:
        result = "SLAM"

    return result, sisr_score, slam_score

# Exemple d'utilisation
if __name__ == "__main__":
    description = input("Décrivez vos préférences : ")
    result, sisr_score, slam_score = classify(description)
    print(f"Orientation suggérée : {result}")
    print(f"Score SISR : {sisr_score:.2f}%")
    print(f"Score SLAM : {slam_score:.2f}%")
