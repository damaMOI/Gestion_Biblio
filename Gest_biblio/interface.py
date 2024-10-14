import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Bibliotheque import Livre, Utilisateur, Pret, Bibliotheque

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Système de Gestion de Bibliothèque")
        self.geometry("600x400")
        self.bibliotheque = Bibliotheque()
        self.create_widgets()

    def create_widgets(self):
        self.create_section("Gestion des Livres", [
            ("Ajouter Livre", self.ajouter_livre),
            ("Afficher Livres", self.afficher_livres)
        ])
        
        self.create_section("Gestion des Utilisateurs", [
            ("Ajouter Utilisateur", self.ajouter_utilisateur),
            ("Afficher Amendes", self.afficher_amendes)
        ])
        
        self.create_section("Prêts et Retours", [
            ("Emprunter Livre", self.emprunter_livre),
            ("Retourner Livre", self.retourner_livre)
        ])

    def create_section(self, title, buttons):
        frame = tk.Frame(self)
        frame.pack(pady=10, fill=tk.X)
        tk.Label(frame, text=title, font=("Arial", 16)).pack()
        for text, command in buttons:
            tk.Button(frame, text=text, command=command).pack(pady=5)

    def create_input_window(self, title, fields, command):
        window = tk.Toplevel(self)
        window.title(title)
        entries = {}
        for field in fields:
            tk.Label(window, text=field).pack()
            entry = tk.Entry(window)
            entry.pack()
            entries[field] = entry
        tk.Button(window, text="Valider", command=lambda: command(entries, window)).pack()

    def ajouter_livre(self):
        self.create_input_window("Ajouter un Livre", 
                                 ["ID Livre", "Titre", "Auteur"],
                                 self.enregistrer_livre)

    def enregistrer_livre(self, entries, window):
        try:
            id_livre = int(entries["ID Livre"].get())
            titre = entries["Titre"].get()
            auteur = entries["Auteur"].get()
            livre = Livre(id_livre, titre, auteur)
            self.bibliotheque.ajouter_livre(livre)
            messagebox.showinfo("Succès", "Livre ajouté avec succès !")
            window.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "ID Livre doit être un nombre entier.")

    def afficher_livres(self):
        livres = self.bibliotheque.livres
        if not livres:
            messagebox.showinfo("Livres", "Aucun livre dans la bibliothèque.")
        else:
            liste_livres = "\n".join([str(livre) for livre in livres])
            messagebox.showinfo("Livres", liste_livres)

    def ajouter_utilisateur(self):
        self.create_input_window("Ajouter un Utilisateur", 
                                 ["ID Utilisateur", "Nom", "Prénom"],
                                 self.enregistrer_utilisateur)

    def enregistrer_utilisateur(self, entries, window):
        try:
            id_utilisateur = int(entries["ID Utilisateur"].get())
            nom = entries["Nom"].get()
            prenom = entries["Prénom"].get()
            utilisateur = Utilisateur(id_utilisateur, nom, prenom)
            self.bibliotheque.ajouter_utilisateur(utilisateur)
            messagebox.showinfo("Succès", "Utilisateur ajouté avec succès !")
            window.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "ID Utilisateur doit être un nombre entier.")

    def emprunter_livre(self):
        self.create_input_window("Emprunter un Livre", 
                                 ["ID Utilisateur", "ID Livre"],
                                 self.enregistrer_emprunt)

    def enregistrer_emprunt(self, entries, window):
        try:
            id_utilisateur = int(entries["ID Utilisateur"].get())
            id_livre = int(entries["ID Livre"].get())
            utilisateur = next((u for u in self.bibliotheque.utilisateurs if u.id_utilisateur == id_utilisateur), None)
            livre = next((l for l in self.bibliotheque.livres if l.id_livre == id_livre), None)
            if utilisateur and livre and livre.disponible:
                pret = Pret(len(self.bibliotheque.prets) + 1, utilisateur, livre, datetime.now())
                self.bibliotheque.ajouter_pret(pret)
                messagebox.showinfo("Succès", f"{livre.titre} a été emprunté par {utilisateur.nom} {utilisateur.prenom}.")
                window.destroy()
            else:
                messagebox.showerror("Erreur", "Livre non disponible ou utilisateur non trouvé.")
        except ValueError:
            messagebox.showerror("Erreur", "Les IDs doivent être des nombres entiers.")

    def retourner_livre(self):
        self.create_input_window("Retourner un Livre", 
                                 ["ID Prêt"],
                                 self.enregistrer_retour)

    def enregistrer_retour(self, entries, window):
        try:
            id_pret = int(entries["ID Prêt"].get())
            self.bibliotheque.retourner_pret(id_pret)
            messagebox.showinfo("Succès", "Livre retourné avec succès.")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def afficher_amendes(self):
        utilisateurs = self.bibliotheque.utilisateurs
        amendes = "\n".join([u.afficher_amende() for u in utilisateurs if u.amendes > 0])
        if amendes:
            messagebox.showinfo("Amendes", amendes)
        else:
            messagebox.showinfo("Amendes", "Aucune amende en cours.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
