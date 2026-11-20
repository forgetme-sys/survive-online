import tkinter as tk
import random

mots = ["CHAT", "CHIEN", "POMME", "SOLEIL", "MAISON",
        "LIVRE", "ECOLE", "BALLON", "ARBRE", "BANANE"]

mot = random.choice(mots)
trouve = ["_"] * len(mot)
erreurs = 0

def jouer():
    global erreurs
    lettre = entree.get().upper()
    entree.delete(0, tk.END)

    if len(lettre) != 1 or not lettre.isalpha():
        message.config(text="Écris une seule lettre !")
        return

    if lettre in mot:
        for i in range(len(mot)):
            if mot[i] == lettre:
                trouve[i] = lettre
        mot_label.config(text=" ".join(trouve))
        message.config(text="✅ Bravo !")
    else:
        erreurs += 1
        message.config(text=f"❌ Erreur {erreurs}/6")

    if "_" not in trouve:
        message.config(text="🏆 Bravo, tu as gagné !")
        bouton.config(state="disabled")

    if erreurs >= 6:
        message.config(text=f"😢 Perdu ! Le mot était {mot}")
        bouton.config(state="disabled")

def nouveau():
    global mot, trouve, erreurs
    mot = random.choice(mots)
    trouve = ["_"] * len(mot)
    erreurs = 0
    mot_label.config(text=" ".join(trouve))
    message.config(text="Choisis une lettre !")
    bouton.config(state="normal")

fenetre = tk.Tk()
fenetre.title("🎮 Jeu du Pendu")
fenetre.geometry("600x450")
fenetre.configure(bg="#17202A")

titre = tk.Label(
    fenetre, text="🎯 JEU DU PENDU",
    bg="#17202A", fg="#FFD700",
    font=("Arial", 28, "bold")
)
titre.pack(pady=25)

mot_label = tk.Label(
    fenetre, text=" ".join(trouve),
    bg="#17202A", fg="white",
    font=("Arial", 30, "bold")
)
mot_label.pack(pady=30)

entree = tk.Entry(
    fenetre, font=("Arial", 20),
    justify="center", width=5
)
entree.pack(pady=10)

bouton = tk.Button(
    fenetre, text="✅ Vérifier",
    command=jouer, bg="#2ECC71",
    fg="white", font=("Arial", 15, "bold")
)
bouton.pack(pady=10)

message = tk.Label(
    fenetre, text="Choisis une lettre !",
    bg="#17202A", fg="#00FF88",
    font=("Arial", 15, "bold")
)
message.pack(pady=15)

tk.Button(
    fenetre, text="🔄 Nouveau mot",
    command=nouveau, bg="#3498DB",
    fg="white", font=("Arial", 13, "bold")
).pack()

fenetre.mainloop()
