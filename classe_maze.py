from random import *

class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """



    """/////////////////////////////////////////////////////////////////
                            - Constructeur -
    /////////////////////////////////////////////////////////////////"""



    def __init__(self, height: int, width: int, empty: bool =False) -> None:
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large.
        L'argument empty indique si le graphe doit être créé avec 
        aucun mur (True), ou avec tous les murs (False).

        Args:
            height (int): Nombre de lignes du labyrinthe
            width (int): Nombre de colonnes du labyrinthe
            empty (bool, optional): Le labyrinthe sera créé sans aucun mur (True), 
                                    l'inverse (False) par défaut.
        """
        self.height    = height
        self.width     = width
        self.empty     = empty
        #Par défaut, on initialise le labyrinthe avec des ensembles vides
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)} 
        if empty:
            #Pour toutes les cellules.
            for i in range(self.height):
                for j in range(self.width):       
                    #On vérifie que ses voisins ne sont pas en dehors du laby.              
                    if (i - 1) >= 0:                            
                        #Si c'est ok on les ajoute à la cellule actuelle.
                        self.neighbors[(i,j)].add((i-1,j))      
                    if (j + 1) < self.width:
                        self.neighbors[(i,j)].add((i,j+1))
                    if (i + 1) < self.height:
                        self.neighbors[(i,j)].add((i+1,j))
                    if (j - 1) >= 0:
                        self.neighbors[(i,j)].add((i,j-1))
        return



    """/////////////////////////////////////////////////////////////////
                        - Méthodes d'affichage -
    /////////////////////////////////////////////////////////////////"""



    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt
    


    """/////////////////////////////////////////////////////////////////
                            - Méthodes d'accès -
    /////////////////////////////////////////////////////////////////"""



    def get_cells(self) -> list:
        """
        Retourne la liste de toutes les cellules de la grille du labyrinthe
        """
        L = []
        for i in range(self.height):
            for j in range(self.width):
                L.append((i,j))
        return L
    
    def get_walls(self) -> list:
        """
        Retourne la liste de tous les murs du laby sous la forme d'une liste
        de tuples de cellules.
        """
        L = []
        for i in range(self.height):
            for j in range(self.width):
                if j+1 < self.width and (i,j+1) not in self.neighbors[(i,j)]:
                    L.append([(i,j), (i,j+1)])
                if i+1 < self.height and (i+1,j) not in self.neighbors[(i,j)]:
                    L.append([(i,j), (i+1,j)])
        return L
    
    def get_contiguous_cells(self, c: tuple) -> list:
        """
        Retourne la liste des cellules contigües à c dans la grille 
        (sans s occuper des éventuels murs).

        Args:
            c (tuple): Cellule visée (i, j)

        Returns:
            list: Liste des cellules contigües.
        """
        L = []
        i = c[0]
        j = c[1]
        #On vérifie que les cellules ne soient pas en dehors du laby.              
        if (i - 1) >= 0:                            
            #Si c'est ok on les ajoute à la liste.
            L.append((i-1,j))      
        if (i + 1) < self.height:
            L.append((i+1,j))
        if (j - 1) >= 0:
            L.append((i,j-1))
        if (j + 1) < self.width:
            L.append((i,j+1))
        return L
        
    def get_reachable_cells(self, c: tuple) -> list:
        """
        Retourne la liste des cellules accessibles depuis c (c est-à-dire 
        les cellules contiguës à c qui sont dans le voisinage de c)
        
        Args:
            c (tuple): Cellule visée (i, j)

        Returns:
            list: Liste des cellules accessibles.
        """
        L = []
        i = c[0]
        j = c[1]
        #On vérifie que les cellules ne soient pas en dehors du laby et si elles
        # sont dans le voisinage de c.              
        if (i - 1) >= 0 and ( (i-1,j) in self.neighbors[(i,j)] and (i,j) in self.neighbors[(i-1,j)] ):                            
            #Si c'est ok on les ajoute à la liste.
            L.append((i-1,j))      
        if (i + 1) < self.height and ( (i+1,j) in self.neighbors[(i,j)] and (i,j) in self.neighbors[(i+1,j)] ):
            L.append((i+1,j))
        if (j - 1) >= 0 and ( (i,j-1) in self.neighbors[(i,j)] and (i,j) in self.neighbors[(i,j-1)] ):
            L.append((i,j-1))
        if (j + 1) < self.width and ( (i,j+1) in self.neighbors[(i,j)] and (i,j) in self.neighbors[(i,j+1)] ):
            L.append((i,j+1))
        return L



    """/////////////////////////////////////////////////////////////////
                        - Méthodes de modification -
    /////////////////////////////////////////////////////////////////"""



    def add_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Permet d'ajouter un mur entre une cellule(c1) et une cellule(c2).

        Args:
            c1 (tuple): Première coordonnée de cellule (i, j)
            c2 (tuple): Deuxième coordonnée de cellule (i, j)
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées ne sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire
        return

    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Permet de supprimer un mur entre une cellule(c1) et une cellule(c2).

        Args:
            c1 (tuple): Première coordonnée de cellule (i, j)
            c2 (tuple): Deuxième coordonnée de cellule (i, j)
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées ne sont pas compatibles avec les dimensions du labyrinthe"
        # Suppression du mur
        if c2 not in self.neighbors[c1]:      # Si c2 n'est pas déjà dans les voisines de c1
            self.neighbors[c1].add(c2)      # on l'ajoute
        if c1 not in self.neighbors[c2]:      # Si c3 n'est pas déjà dans les voisines de c2
            self.neighbors[c2].add(c1)      # on l'ajoute
        return

    def fill(self) -> None:
        """
        Ajoute tous les murs possible dans le labyrinthe.
        """
        for cell in self.neighbors.keys():
            self.neighbors[cell] = set()
        return
    
    def be_empty(self) -> None:
        """
        Supprime tous les murs du labyrinthe.

        On va se baser sur le code du constructeur de la classe
        en l'adaptant pour qu'il vérifie si il n'y a pas déjà de
        passage d'une cellule à l'autre. Cela évitera les voisins
        en double dans certaines cellules.
        """
        for i in range(self.height):
            for j in range(self.width):       
                #On vérifie que ses voisins ne sont pas en dehors du laby et
                # pas déjà dans la liste des voisins.              
                if (i - 1) >= 0 and (i - 1) not in self.neighbors[(i,j)]:                            
                    #Si c'est ok on les ajoute à la cellule actuelle.
                    self.neighbors[(i,j)].add((i-1,j))      
                if (j + 1) < self.width and (j + 1) not in self.neighbors[(i,j)]:
                    self.neighbors[(i,j)].add((i,j+1))
                if (i + 1) < self.height and (i + 1) not in self.neighbors[(i,j)]:
                    self.neighbors[(i,j)].add((i+1,j))
                if (j - 1) >= 0 and (j - 1) not in self.neighbors[(i,j)]:
                    self.neighbors[(i,j)].add((i,j-1))
        return
    
        

    """/////////////////////////////////////////////////////////////////
                           - Méthodes de classe -
    /////////////////////////////////////////////////////////////////"""



    @classmethod
    def gen_btree(cls, h: int, w: int) -> object:
        """
        Génère un labyrinthe à h lignes et w colonnes, en utilisant l algorithme 
        de construction par arbre binaire.
        
        On fera attention à vérifier si les cellules adjacentes sont bien dans la 
        grille avant de tenter de supprimer un mur.

        Args:
            h (int): Nombre de lignes du laby
            w (int): Nombre de colonnes du laby

        Returns:
            object: Le labyrinthe
        """
        # On initialise un laby plein
        laby = Maze(h, w, False)
        # Pour toutes les cellules du laby
        for i in range(laby.height):
            for j in range(laby.width):
                # Si les deux murs EST et SUD sont présents
                if (i,j+1) not in laby.neighbors[(i,j)] and (i+1,j) not in laby.neighbors[(i,j)] and j+1 < w and i+1 < h:
                    # On choisi aléatoirement quel mur enlever
                    temp = randint(0,1)
                    if temp == 1:
                        # Mur EST
                        laby.neighbors[(i,j)].add((i,j+1))
                        laby.neighbors[(i,j+1)].add((i,j))
                    if temp == 0:
                        # Mur SUD
                        laby.neighbors[(i,j)].add((i+1,j))
                        laby.neighbors[(i+1,j)].add((i,j))
                # Si il n'y a qu'un seul des deux murs ou aucun
                else:
                    # Si il n'y a que le mur EST
                    if (i,j+1) not in laby.neighbors[(i,j)] and j+1 < w:
                        laby.neighbors[(i,j)].add((i,j+1))
                        laby.neighbors[(i,j+1)].add((i,j))
                    # Si il n'y a que le mur SUD
                    if (i+1,j) not in laby.neighbors[(i,j)] and i+1 < h:
                        laby.neighbors[(i,j)].add((i+1,j))
                        laby.neighbors[(i+1,j)].add((i,j))
        return laby
    
    @classmethod
    def gen_sidewinder(cls, h: int, w: int) -> object:
        """
        Génère une labyrinthe à h lignes et w colonnes, en utilisant l algorithme 
        de construction par arbre binaire.

        Args:
            h (int): Nombre de lignes du laby
            w (int): Nombre de colonnes du laby

        Returns:
            object: Le labyrinthe généré
        """
        # On initialise un laby plein
        laby = Maze(h, w, False)
        for i in range(h-1):
            #On initialise une séquence vide (liste)
            seq = []
            for j in range(w-1):
                # On initialise la variable dernière cellule qui nous servira pour récupérer
                # la dernière cellule de la séquence
                lastCell = (i,j+1)
                seq.append((i,j))
                # Pile ou face
                if randint(0,1) == 1:
                    # Si pile on casse le mur EST
                    laby.neighbors[(i,j)].add((i,j+1))
                    laby.neighbors[(i,j+1)].add((i,j))
                else:
                    # Si face on casse le mur SUD d'une cellule de la séquence choisie au hasard
                    randomCell = choice(seq)
                    laby.neighbors[randomCell].add((randomCell[0]+1, randomCell[1]))
                    laby.neighbors[(randomCell[0]+1, randomCell[1])].add(randomCell)
                    # On réinitialise la séquence
                    seq = []
            # On ajoute la dernière cellule à la séquence
            seq.append(lastCell)
            # On casse le mur SUD d'une cellule de la séquence choisie au hasard
            randomCell = choice(seq)
            laby.neighbors[randomCell].add((randomCell[0]+1, randomCell[1]))
            laby.neighbors[(randomCell[0]+1, randomCell[1])].add(randomCell)
        # On casse tous les murs EST de la dernière ligne
        for j in range(w-1):
            laby.neighbors[(h-1,j)].add((h-1,j+1))
            laby.neighbors[(h-1,j+1)].add((h-1,j))
        return laby
        
    @classmethod
    def gen_fusion(cls, h: int, w: int) -> object:
        """
        Génère un labyrinthe, à h lignes et w colonnes, parfait, avec l algorithme
        de fusion de chemin.

        Args:
            h (int): Nombre de lignes du laby
            w (int): Nombre de colonnes du laby

        Returns:
            object: Le labyrinthe généré
        """                
        # On initialise un laby plein
        laby = Maze(h, w, False)
        dictLabel = {}
        intLabel = 1
        for i in range(h):
            for j in range(w):
                dictLabel[(i,j)] = intLabel
                intLabel += 1
        listWalls = laby.get_walls()
        shuffle(listWalls)
        
        # Pour chaque mur de la liste
        for wall in listWalls:
            if dictLabel[wall[0]] != dictLabel[wall[1]]:
                laby.neighbors[wall[0]].add(wall[1])
                laby.neighbors[wall[1]].add(wall[0])
                # Pile ou face
                if randint(0,1) == 1:
                    labelAutreCell = dictLabel[wall[1]]
                    dictLabel[wall[1]] = dictLabel[wall[0]]
                    for cell in dictLabel.keys():
                        if dictLabel[cell] == labelAutreCell:
                            dictLabel[cell] = dictLabel[wall[0]]
                else:
                    labelAutreCell = dictLabel[wall[0]]
                    dictLabel[wall[0]] = dictLabel[wall[1]]
                    for cell in dictLabel.keys():
                        if dictLabel[cell] == labelAutreCell:
                            dictLabel[cell] = dictLabel[wall[1]]
        return laby