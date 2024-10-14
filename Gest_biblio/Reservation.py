import datetime
class Reservation:
    def __init__(self, id_reservation, utilisateur, livre):
        self.id_reservation = id_reservation
        self.utilisateur = utilisateur
        self.livre = livre
        self.active = True
        self.date_creation = datetime.now()  # Ajout d'une date de création

    def to_dict(self):
        return {
            "id_reservation": self.id_reservation,
            "utilisateur": self.utilisateur.to_dict(),
            "livre": self.livre.to_dict(),
            "active": self.active,
            "date_creation": self.date_creation.isoformat()
        }

    def __str__(self):
        status = "active" if self.active else "annulée"
        return f"Réservation {self.id_reservation} ({status}) - Utilisateur: {self.utilisateur.nom} {self.utilisateur.prenom}, Livre: {self.livre.titre}"

    def annuler(self):
        if self.active:
            self.active = False
            print(f"La réservation {self.id_reservation} a été annulée.")
        else:
            print(f"La réservation {self.id_reservation} est déjà annulée.")

    def notifier_disponibilite(self):
        if self.active:
            print(f"Le livre '{self.livre.titre}' est maintenant disponible pour {self.utilisateur.nom} {self.utilisateur.prenom}.")
        else:
            print(f"La réservation {self.id_reservation} n'est plus active.")

    def est_active(self):
        return self.active
