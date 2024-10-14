class Livre:
    def __init__(self, id_livre, titre, auteur, disponible=True, annee_publication=None, genre=None):
        self.id_livre = id_livre
        self.titre = titre
        self.auteur = auteur
        self.disponible = disponible
        self.annee_publication = annee_publication
        self.genre = genre
        self.emprunts = []  # Liste pour suivre l'historique des emprunts

    def __str__(self):
        status = "Disponible" if self.disponible else "Non disponible"
        return f"Livre {self.id_livre} - '{self.titre}' par {self.auteur} ({status})"

    def __repr__(self):
        return f"Livre(id_livre={self.id_livre}, titre='{self.titre}', auteur='{self.auteur}', disponible={self.disponible})"

    def to_dict(self):
        return {
            "id_livre": self.id_livre,
            "titre": self.titre,
            "auteur": self.auteur,
            "disponible": self.disponible,
            "annee_publication": self.annee_publication,
            "genre": self.genre
        }

    def modifier_livre(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Attention: L'attribut '{key}' n'existe pas pour ce livre.")

    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        else:
            print(f"Le livre '{self.titre}' n'est pas disponible pour l'emprunt.")
            return False

    def retourner(self):
        if not self.disponible:
            self.disponible = True
            print(f"Le livre '{self.titre}' a été retourné avec succès.")
        else:
            print(f"Erreur: Le livre '{self.titre}' est déjà marqué comme disponible.")

    def ajouter_emprunt(self, emprunt):
        self.emprunts.append(emprunt)

    def afficher_historique_emprunts(self):
        if not self.emprunts:
            print(f"Le livre '{self.titre}' n'a pas encore été emprunté.")
        else:
            print(f"Historique des emprunts pour '{self.titre}':")
            for emprunt in self.emprunts:
                print(f"- Emprunté par {emprunt.utilisateur.nom} le {emprunt.date_emprunt.strftime('%Y-%m-%d')}")
