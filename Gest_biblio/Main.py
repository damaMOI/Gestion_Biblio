from Bibliotheque import Bibliotheque, Livre, Utilisateur, Pret, Reservation
from datetime import datetime, timedelta

def creer_livres():
    return [
        Livre(1, "1984", "George Orwell"),
        Livre(2, "Paris Ville Lumière", "Marie Schoepfer")
    ]

def creer_utilisateurs():
    return [
        Utilisateur(1, "Dupont", "Marie", limite_prets=3),
        Utilisateur(2, "Laporte", "Jean")
    ]

def main():
    bibliotheque = Bibliotheque()

    # Ajout de livres
    livres = creer_livres()
    for livre in livres:
        bibliotheque.ajouter_livre(livre)
    print("Livres ajoutés à la bibliothèque.")

    # Ajout d'utilisateurs
    utilisateurs = creer_utilisateurs()
    for utilisateur in utilisateurs:
        bibliotheque.ajouter_utilisateur(utilisateur)
    print("Utilisateurs ajoutés à la bibliothèque.")

    # Prêt d'un livre
    date_emprunt = datetime.now()
    pret1 = Pret(1, utilisateurs[0], livres[0], date_emprunt)
    bibliotheque.ajouter_pret(pret1)
    print(f"Livre '{livres[0].titre}' emprunté par {utilisateurs[0].nom}.")

    # Réservation d'un livre
    reservation1 = Reservation(1, utilisateurs[1], livres[0])
    bibliotheque.ajouter_reservation(reservation1)
    print(f"Livre '{livres[0].titre}' réservé par {utilisateurs[1].nom}.")

    # Sauvegarde des données dans un fichier JSON
    bibliotheque.sauvegarder_donnees("bibliotheque.json")
    print("Données sauvegardées dans bibliotheque.json")

    # Simulation d'un retour de livre avec retard
    date_retour = date_emprunt + timedelta(days=bibliotheque.duree_maximale + 5)  # 5 jours de retard
    pret1.date_retour = date_retour
    bibliotheque.retourner_pret(1)

    # Afficher les amendes des utilisateurs
    print("\nAmendes des utilisateurs :")
    bibliotheque.afficher_amendes_utilisateurs()

    # Exporter les statistiques
    bibliotheque.exporter_statistiques("statistiques_bibliotheque.json")
    print("Statistiques exportées dans statistiques_bibliotheque.json")

if __name__ == "__main__":
    main()
