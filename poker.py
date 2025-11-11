import random

class Carte:
    noms_couleurs = ['trèfle', 'carreau', 'cœur', 'pique']
    noms_valeurs = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', '10', 'valet', 'dame', 'roi', 'as']
    
    def __init__(self, couleur, valeur):
        self.couleur, self.valeur = couleur, valeur
    
    def __repr__(self):
        return Carte.noms_valeurs[self.valeur] + " de " + Carte.noms_couleurs[self.couleur]
    
    def __lt__(self, other):
        if self.valeur < other.valeur:
            return True
        elif self.valeur == other.valeur:
            return self.couleur < other.couleur
        else:
            return False

class Paquet:
    def __init__(self):
        self.cartes = []
        for couleur in range(4):
            for valeur in range(2, 15):
                self.cartes.append(Carte(couleur, valeur))
    
    def __repr__(self):
        return ", ".join(str(carte) for carte in self.cartes)
    
    def distribuer_carte(self):
        return self.cartes.pop() if self.cartes else None
    
    def ajouter_carte(self, carte):
        self.cartes.append(carte)
    
    def battre(self):
        random.shuffle(self.cartes)
    
    def distribuer_main(self, etiquette, n):
        main = Main(etiquette)
        for i in range(n):
            carte = self.distribuer_carte()
            if carte:
                main.cartes.append(carte)
        return main

class Main(Paquet):
    def __init__(self, etiquette=None):
        self.etiquette, self.cartes = etiquette, []
    
    def __repr__(self):
        cartes_str = ", ".join(str(carte) for carte in self.cartes)
        return self.etiquette + ": " + cartes_str if self.etiquette else "Main: " + cartes_str
    
    def tri(self):
        n = len(self.cartes)
        for i in range(n):
            indice_min = i
            for j in range(i + 1, n):
                if self.cartes[j] < self.cartes[indice_min]:
                    indice_min = j
            self.cartes[i], self.cartes[indice_min] = self.cartes[indice_min], self.cartes[i]
    
    def nom_combinaison(self, score):
        noms = {0:"carte haute", 1:"paire", 2:"double paire", 3:"brelan", 4:"quinte", 
                5:"couleur", 6:"full", 7:"carré", 8:"quinte flush"}
        return noms.get(score, "inconnu")
    
    def famille(self):
        valeurs = [c.valeur for c in self.cartes]
        bilan = []
        for valeur in set(valeurs):
            count = valeurs.count(valeur)
            if count >= 2: 
                bilan.append(count)
        bilan.sort(reverse=True)
        if len(bilan) >= 1 and bilan[0] == 4: 
            return 7
        if len(bilan) >= 2 and bilan[0] == 3 and bilan[1] == 2: 
            return 6
        if len(bilan) >= 1 and bilan[0] == 3: 
            return 3
        if len(bilan) >= 2 and bilan[0] == 2 and bilan[1] == 2: 
            return 2
        if len(bilan) >= 1 and bilan[0] == 2: 
            return 1
        return 0
    
    def quinte(self):
        valeurs = []
        for carte in self.cartes:
            if carte.valeur not in valeurs:
                valeurs.append(carte.valeur)

        main_temp = Main()
        for valeur in valeurs:
            main_temp.cartes.append(Carte(0, valeur))
        main_temp.tri()

        valeurs_triees = []
        for carte in main_temp.cartes:
            valeurs_triees.append(carte.valeur)

        for i in range(len(valeurs_triees) - 4):
            est_quinte = True
            for j in range(5):
                if valeurs_triees[i + j] != valeurs_triees[i] + j:
                    est_quinte = False
                    break
            if est_quinte:
                return True

        if 14 in valeurs_triees:
            a_2_trouve = True
            for val in [2, 3, 4, 5]:
                if val not in valeurs_triees:
                    a_2_trouve = False
                    break
            if a_2_trouve:
                return True

        if 14 in valeurs_triees:
            dix_a_trouve = True
            for val in [10, 11, 12, 13]:
                if val not in valeurs_triees:
                    dix_a_trouve = False
                    break
            if a_2_trouve:
                return True
        
        return False
    
    def couleur(self):
        couleurs = [c.couleur for c in self.cartes]
        for couleur in set(couleurs):
            if couleurs.count(couleur) >= 5:
                return True
        return False
    
    def quinte_flush(self):
        for couleur in set(c.couleur for c in self.cartes):
            cartes_couleur = [c for c in self.cartes if c.couleur == couleur]
            if len(cartes_couleur) >= 5:
                main_temp = Main()
                main_temp.cartes = cartes_couleur
                if main_temp.quinte(): 
                    return True
        return False
    
    def score(self):
        if self.quinte_flush(): 
            return 8, "quinte flush"
        if self.couleur(): 
            return 5, "couleur"
        if self.quinte(): 
            return 4, "quinte"
        score_famille = self.famille()
        return score_famille, self.nom_combinaison(score_famille)

def comparer_mains(main1, main2):
    score1, nom1 = main1.score()
    score2, nom2 = main2.score()
    etiquette1 = main1.etiquette if main1.etiquette else "Main 1"
    etiquette2 = main2.etiquette if main2.etiquette else "Main 2"
    print(etiquette1 + ": " + str(main1.cartes))
    print("→ " + nom1 + " (score: " + str(score1) + ")")
    print(etiquette2 + ": " + str(main2.cartes))
    print("→ " + nom2 + " (score: " + str(score2) + ")")
    if score1 > score2: 
        return etiquette1 + " gagne avec " + nom1 + " !"
    if score2 > score1: 
        return etiquette2 + " gagne avec " + nom2 + " !"
    return "Égalité ! Les deux mains ont " + nom1

class JeuPoker:
    def __init__(self):
        self.paquet = Paquet()
        self.paquet.battre()
        self.joueur1 = self.paquet.distribuer_main("Joueur 1", 5)
        self.joueur2 = self.paquet.distribuer_main("Joueur 2", 5)
    
    def changer_cartes(self, joueur, indices):
        for i in sorted(indices, reverse=True):
            self.paquet.ajouter_carte(joueur.cartes[i])
            nouvelle_carte = self.paquet.distribuer_carte()
            if nouvelle_carte:
                joueur.cartes[i] = nouvelle_carte
    
    def demander_changement(self, joueur):
        print(joueur.etiquette + ", voici votre main:")

        for i in range(len(joueur.cartes)):
            carte = joueur.cartes[i]
            print(str(i+1) + ": " + str(carte))
        nb = int(input("Combien de cartes souhaitez-vous changer ? (0-3) "))
        if nb < 0 or nb > 3: 
            return []
        indices = []
        for i in range(nb):
            idx = int(input("Position carte " + str(i+1) + ": ")) - 1
            if 0 <= idx < 5: 
                indices.append(idx)
        return indices
 
    def jouer_partie(self):
        print("=== DÉBUT DE LA PARTIE ===")
        print("--- Distribution initiale ---")
        print(self.joueur1)
        print(self.joueur2)
        for joueur, nom in [(self.joueur1, "Joueur 1"), (self.joueur2, "Joueur 2")]:
            print("--- Phase de changement - " + nom + " ---")
            indices = self.demander_changement(joueur)
            if indices:
                self.changer_cartes(joueur, indices)
                print("Nouvelle main: " + str(joueur))
        self.joueur1.tri()
        self.joueur2.tri()
        print("--- Résultat final ---")
        print(comparer_mains(self.joueur1, self.joueur2))

if __name__ == "__main__":
    JeuPoker().jouer_partie()
