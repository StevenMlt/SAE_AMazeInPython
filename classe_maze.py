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
