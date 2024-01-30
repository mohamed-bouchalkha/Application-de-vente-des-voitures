import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import ImageTk, Image
import json


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
    def ajouter_voiture(self, marque, modele, description, prix, image_path):
        nouvelle_voiture = Car(marque, modele, description, prix, image_path)
        self.voitures.append(nouvelle_voiture)
        self.save_data()

    def supprimer_voiture(self, car):
        self.voitures.remove(car)
        self.save_data()


class clientDashboard(ctk.CTk):
    def __init__(self, car_store, client_name, client_lastname):
        super().__init__()

        self.afficher_titre(car_store, client_name, client_lastname)  # Pass the car_store parameter to the afficher_titre method
    def afficher_titre(self, car_store, client_name, client_lastname):  # Add the car_store parameter to the afficher_titre method
        titre_label = ttk.Label(self, text=f" AUTOCARS-TAZA\nBienvenue, {client_name} {client_lastname} ", foreground="#FF4D00", font=("Arial", 24, "bold"))
        titre_label.pack(pady=20)

        self.car_store = car_store
        self.title(" BIENVENU ")

        # Ajouter un logo
        self.chemin_du_logo = "images/remove.png"
        self.afficher_logo()

    def afficher_logo(self):
        try:
            img2_pil = Image.open("images/remove.png")
            img2_pil = img2_pil.resize((300, 280), Image.LANCZOS)
            img2 = ImageTk.PhotoImage(img2_pil)
            l2 = ctk.CTkLabel(master=self, text="", image=img2)
            l2.place(x=100, y=35, anchor=tk.CENTER)

        except Exception as e:
            print(f"Erreur lors du chargement du logo : {e}")

        ttk.Label(self, text="").pack()
        self.notebook = ttk.Notebook(self)

        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="voir les Voitures")
        self.onglet_chercher = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_chercher, text=" Chercher par marque ")
        self.notebook.pack(expand=1, fill="both")
        self.onglet_deconnexion = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_deconnexion, text="Déconnexion")
        logout_button = ctk.CTkButton(self.onglet_deconnexion, text="Déconnexion", command=self.confirm_logout)
        logout_button.pack()
        self.afficher_voitures()
        self.afficher_chercher()
    def logout(self):
            # Fermer la fenêtre principale
            self.destroy()

    def confirm_logout(self):
        result = messagebox.askquestion("Déconnexion", "Voulez-vous vraiment sortir de l'application?")
        if result == 'yes':
            self.logout()
    def afficher_chercher(self):
        # Cadre principal
        main_frame = ttk.Frame(self.onglet_chercher)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Cadre pour les éléments de recherche
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, padx=10, pady=3, sticky="w")

        marque_label = ctk.CTkLabel(search_frame, text="la Marque:", font=("Arial", 16), text_color="black")
        marque_label.grid(row=0, column=0, padx=10, pady=3)

        marque_entry = ctk.CTkEntry(search_frame)
        marque_entry.grid(row=0, column=1)

        chercher_button = ctk.CTkButton(search_frame, text="chercher",
                                        command=lambda: self.rechercher_voitures(marque_entry.get()))
        chercher_button.grid(row=0, column=2, padx=10, pady=3)

        # Cadre pour les résultats de la recherche
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    def rechercher_voitures(self, marque):
        # Supprimer uniquement les widgets dans le sous-cadre result_frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        with open("car_data.json", "r") as file:
            data = json.load(file)

        resultats = [voiture for voiture in data["voitures"] if voiture["marque"] == marque]

        if len(resultats) == 0:
            message = f"Aucun résultat trouvé pour la marque {marque}"
            print(message)
            messagebox.showinfo("Information", message)
            return

        col_number = 0  # Numéro de la colonne actuelle

        for i, voiture in enumerate(resultats):
            car_frame = ttk.Frame(self.result_frame, borderwidth=1, relief=tk.RAISED)
            car_frame.grid(row=0, column=col_number, padx=10, pady=10, sticky="w")

            marque_label = ttk.Label(car_frame, text="Marque: " + voiture["marque"], font=("Arial", 25))
            marque_label.pack()

            modele_label = ttk.Label(car_frame, text="Modèle: " + voiture["modele"], font=("Arial", 25))
            modele_label.pack()

            description_label = ttk.Label(car_frame, text="Description: " + voiture["description"], font=("Arial", 25))
            description_label.pack()

            prix_label = ttk.Label(car_frame, text="Prix: " + str(voiture["prix"]) + " DH", font=("Arial", 25))
            prix_label.pack()

            image_path = voiture["image_path"]
            try:
                image = Image.open(image_path)
                image = image.resize((200, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = ttk.Label(car_frame, image=photo)
                image_label.image = photo
                image_label.pack()
            except Exception as e:
                print(
                    f"Erreur lors du chargement de l'image pour la voiture {voiture['marque']} {voiture['modele']}: {e}")
                continue

            col_number += 1  # Passer à la colonne suivante pour la prochaine voiture

            # Add "Consulter" button for each search result
            consulter_button = ctk.CTkButton(car_frame, text="Consulter",
                                             command=lambda v=voiture: self.consulter_voiture(v))
            consulter_button.pack()

    def consulter_voiture(self, voiture):
        # Effacer les anciennes informations dans le frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Afficher les informations détaillées de la voiture
        ttk.Label(self.result_frame, text=f"Marque : {voiture['marque']}", font=("Arial", 16)).pack()
        ttk.Label(self.result_frame, text=f"Modèle : {voiture['modele']}", font=("Arial", 16)).pack()
        ttk.Label(self.result_frame, text=f"Description : {voiture['description']}", font=("Arial", 16)).pack()
        ttk.Label(self.result_frame, text=f"Prix : {voiture['prix']} DH", font=("Arial", 16)).pack()
        ttk.Label(self.result_frame, text=f"Localisation de l'agence: ROUTE TAZA-O1", font=("Helvetica", 17),foreground="red").pack()
        ttk.Label(self.result_frame, text=f"Numéro d'administration de l'agence: +2126-37-70-66-74", font=("Helvetica", 17),foreground="red").pack()

        chemin_image = voiture["image_path"]
        try:
            image = Image.open(chemin_image)
            image = image.resize((400, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label_image = ttk.Label(self.result_frame, image=photo)
            label_image.image = photo
            label_image.pack()
        except Exception as e:
            print(f"Erreur lors du chargement de l'image pour la voiture {voiture['marque']} {voiture['modele']} : {e}")

    def create_and_show_detailed_info_window(self, car):
        class DetailedCarInfoWindow(tk.Toplevel):
            def __init__(self, parent, car):
                super().__init__(parent)
                self.title(f"Détails de la voiture {car.marque} {car.modele}")

                # Display detailed information about the car
                ttk.Label(self, text=f"Marque: {car.marque}",font=("Arial", 16)).pack()
                ttk.Label(self, text=f"Modèle: {car.modele}",font=("Arial", 16)).pack()
                ttk.Label(self, text=f"Description: {car.description}",font=("Arial", 16)).pack()
                ttk.Label(self, text=f"Prix: {car.prix} DH",font=("Arial", 16)).pack()
                ttk.Label(self, text=f"Localisation de l'agence: ROUTE TAZA-O1",foreground="red",font=("Helvetica", 18)).pack()
                ttk.Label(self, text=f"Numéro d'administration de l'agence: +2126-37-70-66-74",foreground="red",font=("Helvetica", 18)).pack()

                # Load and display car image
                try:
                    image = Image.open(car.image_path)
                    image = image.resize((400, 300), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    image_label = ttk.Label(self, image=photo)
                    image_label.image = photo
                    image_label.pack()
                except Exception as e:
                    print(f"Erreur lors du chargement de l'image : {e}")

        detail_window = DetailedCarInfoWindow(self, car)
        detail_window.geometry("900x580")

    def afficher_voitures(self):
        # Create a scrollable frame
        car_container = ctk.CTkScrollableFrame(self.onglet_voitures)
        car_container.pack(fill="both", expand=True)

        for i, car in enumerate(self.car_store.voitures):
            car_item = ctk.CTkFrame(car_container)

            # Load and display car image
            image = Image.open(car.image_path)
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            car_image_label = ctk.CTkLabel(car_item, image=photo, text="")
            car_image_label.image = photo
            car_image_label.pack()

            # Display car information
            car_info_label = ctk.CTkLabel(
                car_item,
                text=f"{car.marque} {car.modele}\n{car.description}\nPrix: {car.prix} DH",
                font=("Arial", 12),
            )
            car_info_label.pack()

            # Add a button to delete the car
            consulter_button = ctk.CTkButton(car_item, text="Consulter",
                                             command=lambda car=car: self.create_and_show_detailed_info_window(car))
            consulter_button.pack()

            # Position each car item inline, moving to a new line every 4 items
            car_item.grid(row=i // 4, column=i % 4, padx=10, pady=10)


if __name__ == '__main__':
    car_store = CarStore()
    ctk.set_appearance_mode("System")
    app = clientDashboard(car_store)
    app.geometry("900x580")
    app.mainloop()
