import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from PIL import ImageTk, Image
import json
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import clients

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

    # def acheter_voiture(self, car, nom, adresse, telephone):
    #     information_achat = {
    #         'Nom': nom,
    #         'Adresse': adresse,
    #         'Téléphone': telephone,
    #         'Voiture': f"{car.marque} {car.modele}",
    #         'Prix': car.prix
    #     }
    #     self.save_data()

    def ajouter_voiture(self, marque, modele, description, prix, image_path):
        nouvelle_voiture = Car(marque, modele, description, prix, image_path)
        self.voitures.append(nouvelle_voiture)
        

        self.save_data()


    def supprimer_voiture(self, car):
        self.voitures.remove(car)
        self.save_data()

class AdminDashboard(ctk.CTk):
    def __init__(self, car_store):
        super().__init__()
        ctk.set_appearance_mode("white")

        self.car_store = car_store
        self.title("Tableau de Bord Administrateur")

        self.notebook = ttk.Notebook(self)

        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Liste des Voitures")

        self.onglet_ajouter = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_ajouter, text="     Ajouter      ")
        self.onglet_modifier = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_modifier, text="    modifier     ")
        self.onglet_chercher = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_chercher, text="     chercher      ")
        self.notebook.pack(expand=1, fill="both")
        self.onglet_statistiques = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_statistiques, text=" Statistiques ")
        statistiques_button = ctk.CTkButton(self.onglet_statistiques, text="Afficher Statistiques",command=self.afficher_statistiques)
        statistiques_button.pack()

        # Ajouter l'onglet Déconnexion directement à côté des autres onglets
        self.onglet_deconnexion = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_deconnexion, text="Déconnexion")

        # Ajouter un bouton de déconnexion à côté des autres onglets
        logout_button = ctk.CTkButton(self.onglet_deconnexion, text="Déconnexion", command=self.confirm_logout)
        logout_button.pack()

        self.afficher_voitures()
        self.afficher_ajouter()
        self.afficher_chercher()

    def logout(self):
        # Fermer la fenêtre principale
        self.destroy()

    def confirm_logout(self):
        result = messagebox.askquestion("Déconnexion", "Voulez-vous vraiment sortir de l'application?")
        if result == 'yes':
            self.logout()

    def afficher_statistiques(self):
        # Your existing statistics calculation code
        marques = [voiture.to_dict()['marque'] for voiture in self.car_store.voitures]
        occurrences = {marque: marques.count(marque) for marque in set(marques)}

        # Create a new figure and plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(occurrences.keys(), occurrences.values(), color='skyblue')
        ax.set_xlabel('Marque de voiture')
        ax.set_ylabel('Nombre de voitures')
        ax.set_title('Statistiques par marque')
        ax.tick_params(axis='x', rotation=45)

        # Set y-axis ticks to integers only
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # Create a Tkinter canvas for the plot
        canvas = FigureCanvasTkAgg(fig, master=self.onglet_statistiques)
        canvas.draw()

        # Place the canvas on the Tkinter window
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def afficher_chercher(self):
        # Cadre principal
        main_frame = ttk.Frame(self.onglet_chercher)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Éléments dans le cadre principal
        marque_label = ctk.CTkLabel(main_frame, text="la Marque:", font=("Arial", 16),text_color="black")
        marque_label.grid(row=1, column=0,padx=10,pady=3)

        marque_entry = ctk.CTkEntry(main_frame)
        marque_entry.grid(row=1, column=1)

        chercher_button = ctk.CTkButton(main_frame, text="chercher",
                                        command=lambda: self.rechercher_voitures(marque_entry.get()))
        chercher_button.grid(row=1, column=2,padx=10,pady=3)

        # Cadre pour les résultats de la recherche
        self.result_frame = ttk.Frame(self.onglet_chercher)
        self.result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")



    def rechercher_voitures(self, marque):
        # Supprimer uniquement les widgets dans le sous-cadre result_frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        with open("car_data.json", "r") as file:
            data = json.load(file)

        resultats = [voiture for voiture in data["voitures"] if voiture["marque"] == marque]

        if len(resultats) == 0:
            messagebox.showinfo("Information", f"Aucune voiture de marque {marque} trouvée.")
            return

        row_number = 0  # Numéro de la ligne actuelle
        col_number = 0  # Numéro de la colonne actuelle

        for i, voiture in enumerate(resultats):
            if col_number == 4:
                # Passer à la ligne suivante après chaque groupe de 3 voitures
                row_number += 1
                col_number = 0

            car_frame = ttk.Frame(self.result_frame, borderwidth=1, relief=tk.RAISED)
            car_frame.grid(row=row_number, column=col_number, padx=10, pady=10)

            marque_label = ttk.Label(car_frame, text="Marque: " + voiture["marque"], font=("Arial", 25))
            marque_label.pack()

            modele_label = ttk.Label(car_frame, text="Modèle: " + voiture["modele"], font=("Arial", 25))
            modele_label.pack()

            description_label = ttk.Label(car_frame, text="Description: " + voiture["description"], font=("Arial", 25))
            description_label.pack()

            prix_label = ttk.Label(car_frame, text="Prix: " + str(voiture["prix"])+" DH", font=("Arial", 25))
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
                continue  # Continue to the next iteration if an error occurs with the image loading

            col_number += 1  # Passer à la colonne suivante pour la prochaine voiture

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
            supprimer_button = ctk.CTkButton(car_item, fg_color="#FF4D00", text="Supprimer",
                                         command=lambda car=car: self.supprimer(car))
            supprimer_button.pack()
            space_frame = ttk.Frame(car_item)
            space_frame.pack(pady=5)
            modifier_button = ctk.CTkButton(car_item, text="Modifier", command=lambda car=car: self.modifier(car))
            modifier_button.pack()

            # Position each car item inline, moving to a new line every 4 items
            car_item.grid(row=i // 4, column=i % 4, padx=10, pady=10)


    def afficher_ajouter(self):
        marque_label = ctk.CTkLabel(self.onglet_ajouter, text="la Marque:",text_color="black")
        marque_label.grid(row=0, column=0, padx=10, pady=5)
        marque_entry = ctk.CTkEntry(self.onglet_ajouter)
        marque_entry.grid(row=0, column=1, padx=10, pady=5)

        modele_label = ctk.CTkLabel(self.onglet_ajouter, text="le Modèle:",text_color="black")
        modele_label.grid(row=1, column=0, padx=10, pady=5)
        modele_entry = ctk.CTkEntry(self.onglet_ajouter)
        modele_entry.grid(row=1, column=1, padx=10, pady=5)

        description_label = ctk.CTkLabel(self.onglet_ajouter, text="la Description:",text_color="black")
        description_label.grid(row=2, column=0, padx=10, pady=5)
        description_entry = ctk.CTkEntry(self.onglet_ajouter)
        description_entry.grid(row=2, column=1, padx=10, pady=5)

        prix_label = ctk.CTkLabel(self.onglet_ajouter, text=" le Prix:",text_color="black")
        prix_label.grid(row=3, column=0, padx=10, pady=5)
        prix_entry = ctk.CTkEntry(self.onglet_ajouter)
        prix_entry.grid(row=3, column=1, padx=6, pady=5)

        image_label = ctk.CTkLabel(self.onglet_ajouter, text="Chemin de l'image:",text_color="black")
        image_label.grid(row=4, column=0, padx=10, pady=5)
        image_entry = ctk.CTkEntry(self.onglet_ajouter)
        image_entry.grid(row=4, column=1, padx=10, pady=5)

        parcourir_button = ctk.CTkButton(self.onglet_ajouter, text="Parcourir",command=lambda: self.parcourir_image(image_entry))
        parcourir_button.grid(row=4, column=2, padx=10, pady=5)

        ajouter_button = ctk.CTkButton(self.onglet_ajouter, text="Ajouter",command=lambda: self.ajouter(marque_entry.get(), modele_entry.get(),
                                                                    description_entry.get(), float(prix_entry.get()),
                                                                    image_entry.get()))
        ajouter_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
        self.car_store.save_data()


    def supprimer(self, car):
        self.car_store.supprimer_voiture(car)
        self.onglet_voitures.destroy()
        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Liste des Voitures")
        self.afficher_voitures()
        self.notebook.select(self.onglet_voitures)

    def modifier(self, car):
        # Effacer les champs existants
        for child in self.onglet_ajouter.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                child.delete(0, tk.END)

        # Remplir les champs avec les informations actuelles de la voiture
        marque_label = ctk.CTkLabel(self.onglet_modifier, text="la Marque:",text_color="black")
        marque_label.grid(row=0, column=0, padx=10, pady=5)
        marque_entry = ctk.CTkEntry(self.onglet_modifier)
        marque_entry.insert(0, car.marque)
        marque_entry.grid(row=0, column=1, padx=10, pady=5)

        modele_label = ctk.CTkLabel(self.onglet_modifier, text="le Modèle:",text_color="black")
        modele_label.grid(row=1, column=0, padx=10, pady=5)
        modele_entry = ctk.CTkEntry(self.onglet_modifier)
        modele_entry.insert(0, car.modele)
        modele_entry.grid(row=1, column=1, padx=10, pady=5)

        description_label = ctk.CTkLabel(self.onglet_modifier, text="la Description:",text_color="black")
        description_label.grid(row=2, column=0, padx=10, pady=5)
        description_entry = ctk.CTkEntry(self.onglet_modifier)
        description_entry.insert(0, car.description)
        description_entry.grid(row=2, column=1, padx=10, pady=5)

        prix_label = ctk.CTkLabel(self.onglet_modifier, text=" le Prix:",text_color="black")
        prix_label.grid(row=3, column=0, padx=10, pady=5)
        prix_entry = ctk.CTkEntry(self.onglet_modifier)
        prix_entry.insert(0, car.prix)
        prix_entry.grid(row=3, column=1, padx=10, pady=5)

        image_label = ctk.CTkLabel(self.onglet_modifier, text="Chemin de l'image:",text_color="black")
        image_label.grid(row=4, column=0, padx=10, pady=5)
        image_entry = ctk.CTkEntry(self.onglet_modifier)
        image_entry.insert(0, car.image_path)
        image_entry.grid(row=4, column=1, padx=10, pady=5)

        parcourir_button = ctk.CTkButton(self.onglet_modifier, text="Parcourir",command=lambda: self.parcourir_image(image_entry))
        parcourir_button.grid(row=4, column=2, padx=10, pady=5)

        # Changer la commande du bouton "Ajouter" pour mettre à jour la voiture
        modifier_button = ctk.CTkButton(self.onglet_modifier, text="Modifier",command=lambda: self.modifier_voiture(car, marque_entry.get(),
                                                                              modele_entry.get(),
                                                                              description_entry.get(),
                                                                              float(prix_entry.get()),
                                                                              image_entry.get()))
        modifier_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        # Afficher l'onglet "modifier"
        self.notebook.select(self.onglet_modifier)

    def modifier_voiture(self, car, marque, modele, description, prix, image_path):
        # Mettre à jour l'objet de la voiture avec les nouvelles valeurs
        car.marque = marque
        car.modele = modele
        car.description = description
        car.prix = prix
        car.image_path = image_path

        # Rafraîchir l'onglet "Voitures" pour refléter les modifications
        self.onglet_voitures.destroy()
        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Liste des Voitures")
        self.afficher_voitures()

        self.car_store.save_data()

        # Revenir à l'onglet "Voitures"
        self.notebook.select(self.onglet_voitures)

    def ajouter(self, marque, modele, description, prix, image_path):
        self.car_store.ajouter_voiture(marque, modele, description, prix, image_path)
        self.onglet_voitures.destroy()
        self.onglet_voitures = tk.Frame(self.notebook)
        self.notebook.add(self.onglet_voitures, text="Liste des Voitures")
        self.afficher_voitures()

        # Switch to the "Liste des Voitures" tab
        self.notebook.select(self.onglet_voitures)

    def parcourir_image(self, entry):
        file_path = filedialog.askopenfilename(title="Sélectionner une image",filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif")])
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


if __name__ == '__main__':
    car_store = CarStore()
    app = AdminDashboard(car_store)
    app.geometry("900x580")
    ctk.set_appearance_mode("Light") 
    app.mainloop()
