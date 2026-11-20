import tkinter as tk
from tkinter import messagebox

questions = [
    ("Combien font 2 + 3 ?", ["4", "5", "6"], "5"),
    ("Quelle couleur obtient-on avec bleu + jaune ?", ["Vert", "Rouge", "Noir"], "Vert"),
    ("Combien de pattes a un chien ?", ["2", "4", "6"], "4"),
    ("Quelle est la première lettre de l'alphabet ?", ["A", "B", "C"], "A"),
    ("Combien font 10 - 4 ?", ["5", "6", "7"], "6"),
    ("Quel animal fait « miaou » ?", ["Chien", "Chat", "Vache"], "Chat"),
    ("Combien y a-t-il de jours dans une semaine ?", ["5", "7", "10"], "7"),
    ("Quelle planète est notre maison ?", ["Mars", "Terre", "Jupiter"], "Terre"),
    ("Combien font 3 × 2 ?", ["5", "6", "8"], "6"),
    ("Quel fruit est généralement jaune ?", ["Banane", "Fraise", "Raisin"], "Banane"),
    ("Quelle saison vient après l'été ?", ["Hiver", "Automne", "Printemps"], "Automne"),
    ("Combien de doigts avons-nous sur une main ?", ["4", "5", "6"], "5"),
    ("Quel animal donne du lait ?", ["Vache", "Lion", "Tigre"], "Vache"),
    ("Combien font 8 + 2 ?", ["9", "10", "12"], "10"),
    ("Quelle forme a 3 côtés ?", ["Carré", "Triangle", "Cercle"], "Triangle")
]

score = 0
numero = 0

def afficher_question():
    global numero

    if numero >= len(questions):
        messagebox.showinfo(
            "Bravo !",
            f"Quiz terminé !\n\nTon score : {score}/{len(questions)}"
        )
        return

    question, reponses, bonne = questions[numero]

    question_label.config(
        text=f"Question {numero + 1}/{len(questions)}\n\n{question}"
    )

    for i in range(3):
        boutons[i].config(
            text=reponses[i],
            command=lambda r=reponses[i]: verifier(r)
        )

def verifier(reponse):
    global score, numero

    bonne = questions[numero][2]

    if reponse == bonne:
        score += 1
        resultat.config(
            text="🌟 Bravo ! Bonne réponse !",
            fg="#00FF66"
        )
    else:
        resultat.config(
            text=f"❌ Pas grave ! La réponse était : {bonne}",
            fg="#FF5555"
        )

    numero += 1
    fenetre.after(1000, afficher_question)

def recommencer():
    global score, numero

    score = 0
    numero = 0
    resultat.config(text="Bonne chance !", fg="#00FF66")
    afficher_question()

fenetre = tk.Tk()
fenetre.title("👨‍🏫 Professeur pour enfants")
fenetre.geometry("700x600")
fenetre.configure(bg="#18202A")

titre = tk.Label(
    fenetre,
    text="👨‍🏫 PROFESSEUR POUR ENFANTS",
    bg="#18202A",
    fg="#FFD700",
    font=("Arial", 24, "bold")
)
titre.pack(pady=20)

question_label = tk.Label(
    fenetre,
    text="",
    bg="#18202A",
    fg="white",
    font=("Arial", 19, "bold"),
    wraplength=600
)
question_label.pack(pady=30)

boutons = []

for i in range(3):
    bouton = tk.Button(
        fenetre,
        text="",
        bg="#3498DB",
        fg="white",
        activebackground="#2ECC71",
        font=("Arial", 15, "bold"),
        width=30,
        height=2
    )
    bouton.pack(pady=7)
    boutons.append(bouton)

resultat = tk.Label(
    fenetre,
    text="Bonne chance ! 🎓",
    bg="#18202A",
    fg="#00FF66",
    font=("Arial", 15, "bold")
)
resultat.pack(pady=20)

restart = tk.Button(
    fenetre,
    text="🔄 Recommencer",
    command=recommencer,
    bg="#E67E22",
    fg="white",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=8
)
restart.pack()

afficher_question()
fenetre.mainloop()
