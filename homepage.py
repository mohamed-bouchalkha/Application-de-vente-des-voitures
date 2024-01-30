import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
from tkinter import messagebox
from Adminpage import AdminDashboard, CarStore
from clients import clientDashboard, CarStore
import json

class LoginPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("System")
        customtkinter.set_appearance_mode("Dark")

        self.geometry("600x500")
        self.title('Login')

        self.frame = customtkinter.CTkFrame(master=self, fg_color="black", height=700, width=300)
        self.frame.pack(side="left")
        img1_pil = Image.open("images/bg3.jpg")
        img1_pil = img1_pil.resize((900, 1400), Image.LANCZOS)
        img1 = ImageTk.PhotoImage(img1_pil)
        l1 = customtkinter.CTkLabel(master=self.frame, text="", image=img1)
        l1.place(anchor=tk.CENTER)

        img2_pil = Image.open("images/remove.png")
        img2_pil = img2_pil.resize((300, 280), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2_pil)
        l2 = customtkinter.CTkLabel(master=self, text="", image=img2)
        l2.place(x=450, y=80, anchor=tk.CENTER)

        label = customtkinter.CTkLabel(self, text="WELCOME TO AUTOCARS", font=("Anton", 21), fg_color="transparent", text_color="#FF4D00")
        label.place(x=450, y=150, anchor=tk.CENTER)
        username = customtkinter.CTkLabel(self, text="USERNAME:")
        username.place(x=413, y=220, anchor=tk.CENTER)
        self.entry_username = customtkinter.CTkEntry(self, font=("Arial", 14), width=150)
        self.entry_username.place(x=450, y=245, anchor=tk.CENTER)
        password = customtkinter.CTkLabel(self, text="PASSWORD:")
        password.place(x=413, y=275, anchor=tk.CENTER)
        self.entry_password = customtkinter.CTkEntry(self, font=("Arial", 14), width=150, show="*")
        self.entry_password.place(x=450, y=300, anchor=tk.CENTER)

        button_login = customtkinter.CTkButton(self, text="Login",
                                         font=("Arial", 18),
                                         text_color="black",
                                         command=self.login_button_event,
                                         width=200, height=30,
                                         corner_radius=20,
                                         fg_color="red",
                                         border_spacing=10)
        button_login.place(x=450, y=350, anchor=tk.CENTER)

        button_register = customtkinter.CTkButton(self, text="Register",
                                            font=("Arial", 18),
                                            text_color="black",
                                            command=self.show_register_form,
                                            width=200, height=30,
                                            corner_radius=20,
                                            fg_color="green",
                                            border_spacing=10)
        button_register.place(x=450, y=400, anchor=tk.CENTER)

        self.car_store = CarStore()

    def login_button_event(self):
        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get()
        with open('clients.json', 'r') as file:
            data = json.load(file)
        if entered_username == "root" and entered_password == "1234":
            self.destroy()
            admin_app = AdminDashboard(self.car_store)
            admin_app.geometry("900x580")
            admin_app.mainloop()
        else:
            authenticated = False
            for client in data['clients']:
                if client['username'] == entered_username and client['password'] == entered_password:
                    authenticated = True
                    self.destroy()
                    app = clientDashboard(self.car_store, client['name'], client['lastname'])
                    app.geometry("900x580")
                    app.mainloop()
                    break

            if not authenticated:
                message = "Incorrect username or password. Please try again."
                messagebox.showinfo("Login Status", message)


    def show_register_form(self):
        for widget in self.winfo_children():
            widget.destroy()

        name_label = customtkinter.CTkLabel(self, text="First Name:")
        name_label.place(x=100, y=80)
        self.name_entry = customtkinter.CTkEntry(self, font=("Arial", 14), width=150)
        self.name_entry.place(x=200, y=80)

        lastname_label = customtkinter.CTkLabel(self, text="Last Name:")
        lastname_label.place(x=100, y=120)  
        self.lastname_entry = customtkinter.CTkEntry(self, font=("Arial", 14), width=150)
        self.lastname_entry.place(x=200, y=120)  

        email_label = customtkinter.CTkLabel(self, text="Email:")  
        email_label.place(x=100, y=160)  
        self.email_entry = customtkinter.CTkEntry(self, font=("Arial", 14), width=150)
        self.email_entry.place(x=200, y=160) 

        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.place(x=100, y=200)  
        self.username_entry = customtkinter.CTkEntry(self, font=("Arial", 14), width=150)
        self.username_entry.place(x=200, y=200) 

        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.place(x=100, y=240)  
        self.password_entry = customtkinter.CTkEntry(self, font=("Arial", 14), width=150, show="*")
        self.password_entry.place(x=200, y=240)  

        register_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        register_button.place(x=200, y=280)  # Adjusted y-coordinate
        return_button = customtkinter.CTkButton(self, text="Return to Login", command=self.return_to_login)
        return_button.place(x=360, y=280)  # Adjusted x-coordinate and y-coordinate

    def return_to_login(self):
        self.destroy()  
        login_page = LoginPage() 
        login_page.mainloop()  
    def register(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        email    = self.email_entry.get()
        client_data = { 
            "name": name,
            "lastname": lastname,
            "email"   :email,
            "username": username,
            "password": password

        }
        try:
            with open('clients.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {'clients': []}
        data['clients'].append(client_data)
        with open('clients.json', 'w') as file:
            json.dump(data, file)
        messagebox.showinfo("Registration Status", "Registration successful!")
if __name__ == '__main__':
    login_app = LoginPage()
    login_app.mainloop()
