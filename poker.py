import random

class Carte:
    noms_couleurs = ['trèfle', 'carreau', 'cœur', 'pique']
    noms_valeurs = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', '10', 'valet', 'dame', 'roi', 'as']
    
    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur
    
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
        cartes_str = []
        for carte in self.cartes:
            cartes_str.append(str(carte))
        return ", ".join(cartes_str)
   
    
    def distribuer_carte(self):
        if len(self.cartes) > 0:
            return self.cartes.pop()
        else:
            return None
    
    def ajouter_carte(self, carte):
        self.cartes.append(carte)
    
    def battre(self):
        random.shuffle(self.cartes)
    
    def distribuer_main(self, etiquette, n):
        main = Main(etiquette)
        for _ in range(n):
            carte = self.distribuer_carte()
            if carte:
                main.cartes.append(carte)
        return main




class Main(Paquet):
    def __init__(self, etiquette=None):
        self.etiquette = etiquette
        self.cartes = []
    
    def __repr__(self):
        cartes_str = []
        for carte in self.cartes:
            cartes_str.append(str(carte))
        if self.etiquette:
            return self.etiquette + ": " + ", ".join(cartes_str)
        else:
            return "Main: " + ", ".join(cartes_str)
    
    def tri(self):
        n = len(self.cartes)
        for i in range(n):
            indice_min = i
            for j in range(i + 1, n):
                if self.cartes[j] < self.cartes[indice_min]:
                    indice_min = j
            self.cartes[i], self.cartes[indice_min] = self.cartes[indice_min], self.cartes[i]
    
    def nom_combinaison(self, score):
        noms = {
            0: "carte haute",
            1: "paire", 
            2: "double paire",
            3: "brelan",
            4: "quinte",
            5: "couleur",
            6: "full",
            7: "carré",
            8: "quinte flush"
        }
        return noms.get(score, "inconnu")
    
    def famille(self):
        if len(self.cartes) < 5:
            return 0
            
        listeValeurs = []
        for carte in self.cartes:
            listeValeurs.append(carte.valeur)
        
        bilan = []
        valeurs_deja_vues = []
        
        for valeur in listeValeurs:
            if valeur not in valeurs_deja_vues:
                count = 0
                for v in listeValeurs:
                    if v == valeur:
                        count += 1
                if count >= 2:
                    bilan.append(count)
                valeurs_deja_vues.append(valeur)
        
        n_bilan = len(bilan)
        for i in range(n_bilan):
            for j in range(0, n_bilan-i-1):
                if bilan[j] < bilan[j+1]:
                    bilan[j], bilan[j+1] = bilan[j+1], bilan[j]
        
        if bilan == [4]:
            return 7
        elif bilan == [3, 2]:
            return 6
        elif bilan == [3]:
            return 3
        elif bilan == [2, 2]:
            return 2
        elif bilan == [2]:
            return 1
        else:
            return 0
    
    def quinte(self):
        if len(self.cartes) < 5:
            return False
    
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
            if dix_a_trouve:
                return True
    
        return False
    
    def couleur(self):
        if len(self.cartes) < 5:
            return False
            
        couleurs = []
        for carte in self.cartes:
            couleurs.append(carte.couleur)
        
        for couleur in range(4):
            count = 0
            for c in couleurs:
                if c == couleur:
                    count += 1
            if count == 5:
                return True
        return False
    
    def quinte_flush(self):
        if len(self.cartes) < 5:
            return False
            
        cartes_par_couleur = {}
        for carte in self.cartes:
            if carte.couleur not in cartes_par_couleur:
                cartes_par_couleur[carte.couleur] = []
            cartes_par_couleur[carte.couleur].append(carte)
        
        for couleur in cartes_par_couleur:
            cartes = cartes_par_couleur[couleur]
            if len(cartes) >= 5:
                main_temp = Main()
                main_temp.cartes = cartes
                if main_temp.quinte():
                    return True
        return False
    
    def score(self):
        if len(self.cartes) < 5:
            return 0, "main incomplète"
            
        if self.quinte_flush():
            return 8, "quinte flush"
        elif self.couleur():
            return 5, "couleur"
        elif self.quinte():
            return 4, "quinte"
        else:
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
    elif score2 > score1:
        return etiquette2 + " gagne avec " + nom2 + " !"
    else:
        return "Égalité ! Les deux mains ont " + nom1




class JeuPoker:
    def __init__(self):
        self.paquet = Paquet()
        self.paquet.battre()
        self.joueur1 = None
        self.joueur2 = None
    
    def distribuer_mains_initiales(self):
        self.joueur1 = self.paquet.distribuer_main("Joueur 1", 5)
        self.joueur2 = self.paquet.distribuer_main("Joueur 2", 5)
    
    def changer_cartes(self, joueur, indices):
        indices_tries = sorted(indices, reverse=True)
        
        for i in indices_tries:
            self.paquet.ajouter_carte(joueur.cartes[i])
            nouvelle_carte = self.paquet.distribuer_carte()
            if nouvelle_carte:
                joueur.cartes[i] = nouvelle_carte
    
    def jouer_partie(self):
        print("=== DÉBUT DE LA PARTIE ===")
        
        self.distribuer_mains_initiales()
        
        print("--- Distribution initiale ---")
        print(self.joueur1)
        print(self.joueur2)
        
        print("--- Phase de changement - Joueur 1 ---")
        indices_j1 = self.demander_changement(self.joueur1)
        if indices_j1:
            self.changer_cartes(self.joueur1, indices_j1)
            print("Nouvelle main: " + str(self.joueur1))
        
        print("--- Phase de changement - Joueur 2 ---")
        indices_j2 = self.demander_changement(self.joueur2)
        if indices_j2:
            self.changer_cartes(self.joueur2, indices_j2)
            print("Nouvelle main: " + str(self.joueur2))
        
        self.joueur1.tri()
        self.joueur2.tri()
        
        print("--- Résultat final ---")
        resultat = comparer_mains(self.joueur1, self.joueur2) 
        print(resultat)
    
    def demander_changement(self, joueur):
        print(joueur.etiquette + ", voici votre main:")
        for i in range(len(joueur.cartes)):
            print(str(i+1) + ": " + str(joueur.cartes[i]))
        
        print("Combien de cartes souhaitez-vous changer ? (0-3)")
        nb_changements = int(input())
        if nb_changements < 0 or nb_changements > 3:
            print("Nombre invalide. Aucun changement effectué.")
            return []
            
        if nb_changements == 0:
            return []
            
        indices = []
        print("Entrez les positions des cartes à changer (1-5):")
        for i in range(nb_changements):
            idx = int(input()) - 1
            if 0 <= idx < 5:
                indices.append(idx)
            else:
                print("Position invalide.")
            
        return indices

# Tests
    
print("=== Test jeu ===")
jeu = JeuPoker()
jeu.jouer_partie()