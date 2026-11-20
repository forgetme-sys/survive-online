import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime


class WhatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Python")
        self.root.geometry("900x600")
        self.root.configure(bg="#111b21")

        # Contacts et messages
        self.chats = {
            "Alice": [
                ("Alice", "Salut ! 👋", "10:30"),
                ("Moi", "Salut Alice !", "10:31")
            ],
            "Bob": [
                ("Bob", "Tu vas bien ?", "11:05")
            ],
            "Groupe": [
                ("Alice", "Bienvenue dans le groupe !", "12:00"),
                ("Bob", "Bonjour 👋", "12:01")
            ]
        }

        self.current_chat = "Alice"

        self.create_interface()
        self.load_chat()

    # =========================
    # INTERFACE
    # =========================
    def create_interface(self):

        # ===== GAUCHE =====
        left = tk.Frame(
            self.root,
            bg="#202c33",
            width=300
        )
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # Logo
        header = tk.Frame(
            left,
            bg="#202c33",
            height=70
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="WhatsApp",
            bg="#202c33",
            fg="#25D366",
            font=("Arial", 22, "bold")
        ).pack(
            side="left",
            padx=15,
            pady=15
        )

        # Bouton nouveau chat
        tk.Button(
            header,
            text="+",
            command=self.new_chat,
            bg="#202c33",
            fg="white",
            bd=0,
            font=("Arial", 20)
        ).pack(
            side="right",
            padx=15
        )

        # Recherche
        self.search = tk.Entry(
            left,
            bg="#2a3942",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Arial", 11)
        )

        self.search.pack(
            fill="x",
            padx=10,
            pady=10,
            ipady=8
        )

        self.search.insert(0, "Rechercher")

        # Liste des contacts
        self.chat_list = tk.Listbox(
            left,
            bg="#111b21",
            fg="white",
            selectbackground="#2a3942",
            selectforeground="white",
            bd=0,
            highlightthickness=0,
            font=("Arial", 13)
        )

        self.chat_list.pack(
            fill="both",
            expand=True
        )

        self.chat_list.bind(
            "<<ListboxSelect>>",
            self.select_chat
        )

        self.refresh_chat_list()

        # ===== DROITE =====
        right = tk.Frame(
            self.root,
            bg="#0b141a"
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # En-tête du chat
        self.chat_header = tk.Frame(
            right,
            bg="#202c33",
            height=70
        )

        self.chat_header.pack(
            fill="x"
        )

        self.title_label = tk.Label(
            self.chat_header,
            text="",
            bg="#202c33",
            fg="white",
            font=("Arial", 15, "bold")
        )

        self.title_label.pack(
            anchor="w",
            padx=20,
            pady=(10, 0)
        )

        self.status_label = tk.Label(
            self.chat_header,
            text="en ligne",
            bg="#202c33",
            fg="#aebac1",
            font=("Arial", 9)
        )

        self.status_label.pack(
            anchor="w",
            padx=20
        )

        # Messages
        self.messages = tk.Text(
            right,
            bg="#0b141a",
            fg="white",
            bd=0,
            wrap="word",
            state="disabled",
            font=("Arial", 12),
            padx=20,
            pady=15
        )

        self.messages.pack(
            fill="both",
            expand=True
        )

        # Zone du bas
        bottom = tk.Frame(
            right,
            bg="#202c33"
        )

        bottom.pack(
            fill="x"
        )

        self.message_entry = tk.Entry(
            bottom,
            bg="#2a3942",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Arial", 12)
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10, 5),
            pady=10,
            ipady=10
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        self.send_button = tk.Button(
            bottom,
            text="➤",
            command=self.send_message,
            bg="#25D366",
            fg="white",
            bd=0,
            font=("Arial", 16, "bold"),
            width=4
        )

        self.send_button.pack(
            side="right",
            padx=(5, 10),
            pady=10
        )

    # =========================
    # LISTE DES CONTACTS
    # =========================
    def refresh_chat_list(self):

        self.chat_list.delete(
            0,
            tk.END
        )

        for name in self.chats:
            self.chat_list.insert(
                tk.END,
                "  " + name
            )

    # =========================
    # OUVRIR UN CHAT
    # =========================
    def select_chat(self, event=None):

        selected = self.chat_list.curselection()

        if not selected:
            return

        index = selected[0]

        self.current_chat = list(
            self.chats.keys()
        )[index]

        self.load_chat()

    # =========================
    # AFFICHER LES MESSAGES
    # =========================
    def load_chat(self):

        self.title_label.config(
            text=self.current_chat
        )

        self.status_label.config(
            text="🟢 en ligne"
        )

        self.messages.config(
            state="normal"
        )

        self.messages.delete(
            "1.0",
            tk.END
        )

        for sender, message, time in self.chats[
            self.current_chat
        ]:

            if sender == "Moi":

                self.messages.insert(
                    tk.END,
                    f"\nMoi  {time}\n",
                    "me"
                )

                self.messages.insert(
                    tk.END,
                    f"   {message}\n"
                )

            else:

                self.messages.insert(
                    tk.END,
                    f"\n{sender}  {time}\n",
                    "other"
                )

                self.messages.insert(
                    tk.END,
                    f"   {message}\n"
                )

        self.messages.tag_config(
            "me",
            foreground="#25D366",
            font=("Arial", 10, "bold")
        )

        self.messages.tag_config(
            "other",
            foreground="#53bdeb",
            font=("Arial", 10, "bold")
        )

        self.messages.config(
            state="disabled"
        )

        self.messages.see(
            tk.END
        )

    # =========================
    # ENVOYER MESSAGE
    # =========================
    def send_message(self):

        message = self.message_entry.get().strip()

        if message == "":
            return

        time = datetime.now().strftime("%H:%M")

        self.chats[
            self.current_chat
        ].append(
            ("Moi", message, time)
        )

        self.message_entry.delete(
            0,
            tk.END
        )

        self.load_chat()

    # =========================
    # NOUVEAU CONTACT
    # =========================
    def new_chat(self):

        name = simpledialog.askstring(
            "Nouveau chat",
            "Nom du contact :"
        )

        if name is None:
            return

        name = name.strip()

        if name == "":
            return

        if name in self.chats:

            messagebox.showinfo(
                "WhatsApp",
                "Ce contact existe déjà."
            )

            return

        self.chats[name] = []

        self.refresh_chat_list()

        self.current_chat = name

        index = list(
            self.chats.keys()
        ).index(name)

        self.chat_list.selection_clear(
            0,
            tk.END
        )

        self.chat_list.selection_set(
            index
        )

        self.load_chat()


# =========================
# LANCER L'APPLICATION
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    app = WhatsApp(root)

    root.mainloop()