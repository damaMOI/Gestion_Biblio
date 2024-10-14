from datetime import datetime, timedelta

class Paiement:
    def __init__(self, montant, date, utilisateur):
        self.montant = montant
        self.date = date
        self.utilisateur = utilisateur

class Utilisateur:
    def __init__(self, id_utilisateur, nom, prenom, limite_prets=4):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.prets_actifs = []
        self.limite_prets = limite_prets
        self.amendes = 0
        self.historique_paiements = []

    def to_dict(self):
        return {
            "id_utilisateur": self.id_utilisateur,
            "nom": self.nom,
            "prenom": self.prenom,
            "limite_prets": self.limite_prets
        }
    
    def __str__(self):
        return f"ID: {self.id_utilisateur}, Nom: {self.nom}, Prénom: {self.prenom}, Prêts actifs: {len(self.prets_actifs)}/{self.limite_prets}"

    def peut_emprunter(self):
        return len(self.prets_actifs) < self.limite_prets

    def ajouter_pret_actif(self, pret):
        if self.peut_emprunter():
            self.prets_actifs.append(pret)
        else:
            print(f"L'utilisateur {self.nom} {self.prenom} a atteint sa limite de prêts.")
    
    def retourner_pret(self, pret):
        if pret in self.prets_actifs:
            self.prets_actifs.remove(pret)

    def modifier_utilisateur(self, nom=None, prenom=None):
        if nom:
            self.nom = nom
        if prenom:
            self.prenom = prenom

    def ajouter_amende(self, montant):
        self.amendes += montant

    def payer_amende(self, montant):
        if montant <= self.amendes:
            self.amendes -= montant
        else:
            raise ValueError("Montant du paiement supérieur à l'amende due.")

    def afficher_amende(self):
        return f"Utilisateur {self.nom} {self.prenom} doit {self.amendes} €."
    
    def ajouter_paiement(self, montant):
        paiement = Paiement(montant, datetime.now(), self)
        self.historique_paiements.append(paiement)