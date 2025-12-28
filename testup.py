import tkinter as tk
import random

class Jeu:
    def __init__(self):
        self.nombre = random.randint(1, 100)
        self.fenetre = tk.Tk()
        self.fenetre.title("Devine le nombre")
        self.fenetre.geometry("300x200")
        self.fenetre.resizable(False, False)

        self.label = tk.Label(self.fenetre, text="Devine un nombre entre 1 et 100")
        self.label.pack(pady=10)

        self.entree = tk.Entry(self.fenetre)
        self.entree.pack()

        self.bouton = tk.Button(self.fenetre, text="Valider", command=self.verifier)
        self.bouton.pack(pady=5)

        self.resultat = tk.Label(self.fenetre, text="")
        self.resultat.pack(pady=10)

        self.reset = tk.Button(self.fenetre, text="Rejouer", command=self.rejouer)
        self.reset.pack()

        self.fenetre.mainloop()

    def verifier(self):
        try:
            choix = int(self.entree.get())
            if choix < self.nombre:
                self.resultat.config(text="Trop petit")
            elif choix > self.nombre:
                self.resultat.config(text="Trop grand")
            else:
                self.resultat.config(text="🎉 Gagné !")
        except:
            self.resultat.config(text="Entre un nombre valide")

    def rejouer(self):
        self.nombre = random.randint(1, 100)
        self.entree.delete(0, tk.END)
        self.resultat.config(text="")

Jeu()
