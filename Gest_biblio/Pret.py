from datetime import datetime, timedelta

class Pret:
    def __init__(self, id_pret, utilisateur, livre, date_emprunt=None, duree_max=15, amende_par_jour=0.5):
        self.id_pret = id_pret
        self.utilisateur = utilisateur
        self.livre = livre
        self.date_emprunt = date_emprunt or datetime.now()
        self.date_limite = self.date_emprunt + timedelta(days=duree_max)
        self.date_retour = None
        self.retourne = False
        self.amende_par_jour = amende_par_jour
        self.amende = 0

    def __str__(self):
        status = "Retourné" if self.retourne else "En cours"
        date_retour = self.date_retour.strftime('%Y-%m-%d') if self.date_retour else "Non retourné"
        return f"Prêt {self.id_pret} - Utilisateur: {self.utilisateur.nom} {self.utilisateur.prenom}, " \
               f"Livre: {self.livre.titre}, Date d'emprunt: {self.date_emprunt.strftime('%Y-%m-%d')}, " \
               f"Date limite: {self.date_limite.strftime('%Y-%m-%d')}, Date de retour: {date_retour}, " \
               f"Statut: {status}"

    def to_dict(self):
        return {
            "id_pret": self.id_pret,
            "utilisateur": self.utilisateur.to_dict(),
            "livre": self.livre.to_dict(),
            "date_emprunt": self.date_emprunt.isoformat(),
            "date_limite": self.date_limite.isoformat(),
            "date_retour": self.date_retour.isoformat() if self.date_retour else None,
            "retourne": self.retourne,
            "amende": self.amende
        }

    def retourner_livre(self):
        if not self.retourne:
            self.date_retour = datetime.now()
            self.retourne = True
            self.livre.disponible = True
            self.utilisateur.retourner_pret(self)
            self.calculer_amende()
            if self.amende > 0:
                self.utilisateur.ajouter_amende(self.amende)
            print(f"Livre '{self.livre.titre}' retourné avec succès.")
        else:
            print("Ce prêt a déjà été retourné.")

    def calculer_retard(self):
        if not self.retourne:
            jours_retard = (datetime.now() - self.date_limite).days
        else:
            jours_retard = (self.date_retour - self.date_limite).days
        return max(0, jours_retard)

    def calculer_amende(self):
        jours_retard = self.calculer_retard()
        self.amende = jours_retard * self.amende_par_jour
        return self.amende

    def prolonger(self, jours_supplementaires):
        if not self.retourne and self.calculer_retard() == 0:
            self.date_limite += timedelta(days=jours_supplementaires)
            print(f"Prêt prolongé. Nouvelle date limite : {self.date_limite.strftime('%Y-%m-%d')}")
        else:
            print("Impossible de prolonger ce prêt.")
