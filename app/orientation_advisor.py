class OrientationAdvisor:
    def __init__(self):
        self.sisr_keywords = [
            "réseau", "infrastructure", "sécurité", "système", "virtualisation",
            "cloud", "serveur", "maintenance", "administration"
        ]
        self.slam_keywords = [
            "développement", "programmation", "application", "logiciel", "web",
            "base de données", "mobile", "algorithmique", "interface"
        ]

    def analyze(self, description):
        description = description.lower()
        sisr_count = sum(keyword in description for keyword in self.sisr_keywords)
        slam_count = sum(keyword in description for keyword in self.slam_keywords)

        total = sisr_count + slam_count
        if total == 0:
            return "Indécis", 50, 50

        sisr_score = (sisr_count / total) * 100
        slam_score = (slam_count / total) * 100

        if abs(sisr_score - slam_score) < 10:
            return "Indécis", sisr_score, slam_score
        elif sisr_score > slam_score:
            return "SISR", sisr_score, slam_score
        else:
            return "SLAM", sisr_score, slam_score

    def get_advice(self, result, sisr_score, slam_score):
        if result == "Indécis":
            return "Basé sur votre description, il semble que vous ayez des intérêts dans les deux domaines. " \
                   "Nous vous recommandons d'explorer plus en détail les deux options avant de faire votre choix."
        elif result == "SISR":
            return "Votre profil semble plus orienté vers SISR. Vous semblez avoir un intérêt pour " \
                   "les réseaux, l'infrastructure et l'administration des systèmes."
        else:
            return "Votre profil semble plus orienté vers SLAM. Vous semblez avoir un intérêt pour " \
                   "le développement d'applications et la programmation."

