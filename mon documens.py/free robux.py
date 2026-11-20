import tkinter as tk

robux = 0
pseudo = ""

def commencer():
    global pseudo
    pseudo = compte.get().strip()

    if not pseudo:
        message.config(text="⚠️ Écris ton nom Roblox.")
        return

    login.destroy()
    afficher_app()

def click_robux():
    global robux
    robux += 10
    solde.config(text=f"{robux:,}".replace(",", " "))
    message.config(text="+10 Robux virtuels ✓")

def ouvrir_shop():
    shop = tk.Toplevel(root)
    shop.title("Robux Shop")
    shop.geometry("450x480")
    shop.configure(bg="#f2f2f2")
    shop.resizable(False, False)

    tk.Label(
        shop,
        text="🛒 ROBUX SHOP",
        font=("Arial", 25, "bold"),
        bg="#f2f2f2"
    ).pack(pady=25)

    tk.Label(
        shop,
        text=f"Compte : {pseudo}",
        font=("Arial", 13, "bold"),
        bg="#f2f2f2"
    ).pack(pady=5)

    tk.Label(
        shop,
        text=f"Solde : {robux:,} Robux virtuels".replace(",", " "),
        font=("Arial", 12),
        bg="#f2f2f2"
    ).pack(pady=5)

    for montant in [1000, 2000, 3000]:
        tk.Button(
            shop,
            text=f"ÉCHANGER {montant:,} ROBUX".replace(",", " "),
            font=("Arial", 14, "bold"),
            bg="#00a2ff",
            fg="white",
            relief="flat",
            width=27,
            height=2,
            cursor="hand2",
            command=lambda m=montant: echange(m)
        ).pack(pady=10)

def echange(montant):
    if robux >= montant:
        message.config(
            text=f"Simulation : {montant:,} Robux échangés.".replace(",", " ")
        )
    else:
        message.config(text="❌ Solde virtuel insuffisant.")

def afficher_app():
    global root, solde, message

    root = tk.Tk()
    root.title("Robux Simulator")
    root.geometry("600x550")
    root.configure(bg="#f2f2f2")
    root.resizable(False, False)

    tk.Label(
        root,
        text="ROBLOX",
        font=("Arial", 30, "bold"),
        bg="#f2f2f2"
    ).pack(pady=25)

    tk.Label(
        root,
        text=f"Compte : {pseudo}",
        font=("Arial", 14, "bold"),
        bg="#f2f2f2"
    ).pack()

    tk.Label(
        root,
        text="💰 SOLDE ROBUX",
        font=("Arial", 14, "bold"),
        bg="#f2f2f2"
    ).pack(pady=(25, 5))

    solde = tk.Label(
        root,
        text="0",
        font=("Arial", 42, "bold"),
        bg="#f2f2f2"
    )
    solde.pack()

    tk.Button(
        root,
        text="🖱️ CLICK ROBUX +10",
        font=("Arial", 17, "bold"),
        bg="#00a2ff",
        fg="white",
        relief="flat",
        width=25,
        height=2,
        cursor="hand2",
        command=click_robux
    ).pack(pady=20)

    tk.Button(
        root,
        text="🛒 SHOP / ÉCHANGER",
        font=("Arial", 17, "bold"),
        bg="#222222",
        fg="white",
        relief="flat",
        width=25,
        height=2,
        cursor="hand2",
        command=ouvrir_shop
    ).pack()

    message = tk.Label(
        root,
        text="",
        font=("Arial", 12, "bold"),
        bg="#f2f2f2"
    )
    message.pack(pady=25)

    root.mainloop()


# Écran du compte
login = tk.Tk()
login.title("Connexion - Robux Simulator")
login.geometry("450x300")
login.configure(bg="#f2f2f2")
login.resizable(False, False)

tk.Label(
    login,
    text="ROBLOX",
    font=("Arial", 30, "bold"),
    bg="#f2f2f2"
).pack(pady=30)

tk.Label(
    login,
    text="Écris ton nom de compte Roblox",
    font=("Arial", 13),
    bg="#f2f2f2"
).pack()

compte = tk.Entry(
    login,
    font=("Arial", 16),
    justify="center",
    width=25
)
compte.pack(pady=15)

message = tk.Label(
    login,
    text="",
    font=("Arial", 11),
    bg="#f2f2f2"
)
message.pack()

tk.Button(
    login,
    text="CONTINUER",
    font=("Arial", 15, "bold"),
    bg="#00a2ff",
    fg="white",
    relief="flat",
    width=20,
    height=2,
    command=commencer
).pack(pady=15)

login.mainloop()