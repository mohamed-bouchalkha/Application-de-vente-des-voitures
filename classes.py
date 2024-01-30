import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import ImageTk, Image

class Car:
    def __init__(self, marque, modele, description, prix, image_path):
        self.marque = marque
        self.modele = modele
        self.description = description
        self.prix = prix
        self.image_path = image_path

    def to_dict(self):
        return {
            'marque': self.marque,
            'modele': self.modele,
            'description': self.description,
            'prix': self.prix,
            'image_path': self.image_path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['marque'], data['modele'], data['description'], data['prix'], data['image_path'])

class CarStore:
    def __init__(self):
        self.voitures = []
        self.clients = []
        self.load_data()

    def load_data(self):
        try:
            with open('car_data.json', 'r') as file:
                data = json.load(file)
                self.voitures = [Car.from_dict(car_data) for car_data in data['voitures']]
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {'voitures': [car.to_dict() for car in self.voitures]}
        with open('car_data.json', 'w') as file:
            json.dump(data, file)
class AdminDashboard(ctk.CTk):
    def __init__(self, car_store):
        super().__init__()
        self.car_store = car_store
        self.title("Tableau de Bord Administrateur")

        self.notebook = ttk.Notebook(self)

        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Voitures")

        self.onglet_ajouter = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_ajouter, text="Ajouter")

        self.notebook.pack(expand=1, fill="both")

        self.afficher_voitures()
        self.afficher_ajouter()

    def afficher_voitures(self):
        for i, car in enumerate(self.car_store.voitures):
            car_frame = ctk.CTkFrame(self.onglet_voitures)
            car_frame.pack(pady=10)

            car_label = ctk.CTkLabel(
                car_frame,
                text=f"{car.marque} {car.modele}\n{car.description}\nPrix: {car.prix} euros",
                font=("Arial", 12),
            )
            car_label.pack()

            supprimer_button = ctk.CTkButton(car_frame, text="Supprimer", command=lambda car=car: self.supprimer(car))
            supprimer_button.pack()

    def afficher_ajouter(self):
        marque_label = ctk.CTkLabel(self.onglet_ajouter, text="Marque:")
        marque_label.grid(row=0, column=0)
        marque_entry = ctk.CTkEntry(self.onglet_ajouter)
        marque_entry.grid(row=0, column=1)

        modele_label = ctk.CTkLabel(self.onglet_ajouter, text="Modèle:")
        modele_label.grid(row=1, column=0)
        modele_entry = ctk.CTkEntry(self.onglet_ajouter)
        modele_entry.grid(row=1, column=1)

        description_label = ctk.CTkLabel(self.onglet_ajouter, text="Description:")
        description_label.grid(row=2, column=0)
        description_entry = ctk.CTkEntry(self.onglet_ajouter)
        description_entry.grid(row=2, column=1)

        prix_label = ctk.CTkLabel(self.onglet_ajouter, text="Prix:")
        prix_label.grid(row=3, column=0)
        prix_entry = ctk.CTkEntry(self.onglet_ajouter)
        prix_entry.grid(row=3, column=1)

        ajouter_button = ctk.CTkButton(self.onglet_ajouter, text="Ajouter", command=lambda: self.ajouter(marque_entry.get(), modele_entry.get(), description_entry.get(), float(prix_entry.get())))
        ajouter_button.grid(row=4, column=0, columnspan=2)

    def supprimer(self, car):
        self.car_store.supprimer_voiture(car)
        self.onglet_voitures.destroy()
        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Voitures")
        self.afficher_voitures()

    def ajouter(self, marque, modele, description, prix):
        self.car_store.ajouter_voiture(marque, modele, description, prix)
        self.onglet_voitures.destroy()
        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Voitures")
        self.afficher_voitures()