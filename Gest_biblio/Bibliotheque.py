import json
from datetime import datetime, timedelta

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.utilisateurs = []
        self.prets = []
        self.reservations = []
        self.duree_maximale = 14  # Durée maximale d'un prêt en jours
        self.tarif_amende_par_jour = 1  # Tarif de l'amende par jour de retard

    # Gestion des livres
class Livre:
    def __init__(self, id_livre, titre, auteur, disponible=True, annee_publication=None, genre=None):
        self.id_livre = id_livre
        self.titre = titre
        self.auteur = auteur
        self.disponible = disponible
        self.annee_publication = annee_publication
        self.genre = genre
        self.emprunts = []  # Liste pour suivre l'historique des emprunts

    def ajouter_livre(self, livre):
        self.livres.append(livre)

    def supprimer_livre(self, id_livre):
        self.livres = [livre for livre in self.livres if livre.id_livre != id_livre]

    def modifier_livre(self, id_livre, **kwargs):
        for livre in self.livres:
            if livre.id_livre == id_livre:
                livre.modifier_livre(**kwargs)
                break

    # Gestion des utilisateurs
    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs.append(utilisateur)

    def supprimer_utilisateur(self, id_utilisateur):
        self.utilisateurs = [u for u in self.utilisateurs if u.id_utilisateur != id_utilisateur]

    def modifier_utilisateur(self, id_utilisateur, **kwargs):
        for utilisateur in self.utilisateurs:
            if utilisateur.id_utilisateur == id_utilisateur:
                utilisateur.modifier_utilisateur(**kwargs)
                break

    # Gestion des prêts
    def ajouter_pret(self, pret):
        if pret.livre.disponible and pret.utilisateur.peut_emprunter():
            self.prets.append(pret)
            pret.livre.disponible = False
            pret.utilisateur.ajouter_pret_actif(pret)
        else:
            print(f"Le livre '{pret.livre.titre}' n'est pas disponible pour prêt.")

    def retourner_pret(self, id_pret):
        pret = next((p for p in self.prets if p.id_pret == id_pret and not p.retourne), None)
        if pret:
            pret.retourner_livre()
            amende = self.calculer_amende(pret)
            if amende > 0:
                pret.utilisateur.ajouter_amende(amende)
                print(f"Amende pour {pret.utilisateur.nom} {pret.utilisateur.prenom} : {amende} €.")
            self.notifier_reservation(pret.livre)
        else:
            print(f"Le prêt {id_pret} est déjà retourné ou n'existe pas.")

    def calculer_amende(self, pret):
        date_retour = pret.date_retour or datetime.now()
        date_echeance = pret.date_emprunt + timedelta(days=self.duree_maximale)
        if date_retour > date_echeance:
            jours_de_retard = (date_retour - date_echeance).days
            return jours_de_retard * self.tarif_amende_par_jour
        return 0

    # Gestion des réservations
    def ajouter_reservation(self, reservation):
        if not reservation.livre.disponible:
            self.reservations.append(reservation)
            print(f"Le livre '{reservation.livre.titre}' est réservé par {reservation.utilisateur.nom}.")
        else:
            print(f"Le livre '{reservation.livre.titre}' est déjà disponible.")

    def notifier_reservation(self, livre):
        reservations_actives = [r for r in self.reservations if r.livre == livre and r.active]
        for reservation in reservations_actives[:3]:
            reservation.notifier_disponibilite()
            reservation.annuler()

    def annuler_reservation(self, id_reservation):
        reservation = next((r for r in self.reservations if r.id_reservation == id_reservation and r.active), None)
        if reservation:
            reservation.annuler()
            print(f"La réservation {id_reservation} est annulée.")
        else:
            print(f"La réservation {id_reservation} est déjà annulée ou n'existe pas.")

    # Statistiques et rapports
    def livres_plus_empruntes(self):
        stats_emprunts = {}
        for pret in self.prets:
            livre_id = pret.livre.id_livre
            stats_emprunts[livre_id] = stats_emprunts.get(livre_id, 0) + 1
        return sorted(stats_emprunts.items(), key=lambda x: x[1], reverse=True)

    def utilisateurs_avec_plus_de_prets(self):
        stats_prets = {}
        for pret in self.prets:
            utilisateur_id = pret.utilisateur.id_utilisateur
            stats_prets[utilisateur_id] = stats_prets.get(utilisateur_id, 0) + 1
        return sorted(stats_prets.items(), key=lambda x: x[1], reverse=True)

    def exporter_statistiques(self, fichier):
        stats = {
            'livres_plus_empruntes': self.livres_plus_empruntes(),
            'utilisateurs_plus_prets': self.utilisateurs_avec_plus_de_prets()
        }
        with open(fichier, 'w') as f:
            json.dump(stats, f, indent=4)

    def afficher_amendes_utilisateurs(self):
        for utilisateur in self.utilisateurs:
            if utilisateur.amendes > 0:
                print(utilisateur.afficher_amende())

    # Sauvegarde et chargement des données
    def sauvegarder_donnees(self, nom_fichier="bibliotheque.json"):
        donnees = {
            "livres": [livre.to_dict() for livre in self.livres],
            "utilisateurs": [utilisateur.to_dict() for utilisateur in self.utilisateurs],
            "prets": [pret.to_dict() for pret in self.prets],
            "reservations": [reservation.to_dict() for reservation in self.reservations]
        }
        with open(nom_fichier, 'w') as fichier_json:
            json.dump(donnees, fichier_json, indent=4)
        print(f"Les données ont été sauvegardées dans {nom_fichier}.")

    # Méthode pour charger les données (à implémenter si nécessaire)
    def charger_donnees(self, nom_fichier="bibliotheque.json"):
        # Implémentation à ajouter
        pass
