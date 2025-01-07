def classify(description):
    sisr_keywords = ["serveur", "virtualisation", "réseau"]
    slam_keywords = ["application", "base de données", "développement"]

    sisr_score = sum(word in description for word in sisr_keywords)
    slam_score = sum(word in description for word in slam_keywords)

    if sisr_score > slam_score:
        return "SISR"
    elif slam_score > sisr_score:
        return "SLAM"
    else:
        return "Indécis"

# Exemple
print(classify("J'aime travailler avec des applications web"))
