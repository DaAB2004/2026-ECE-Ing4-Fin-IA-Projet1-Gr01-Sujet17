from dataclasses import dataclass
from typing import List, Tuple
import random

# Une petite classe pour stocker les infos d'un mot à trouver
@dataclass
class WordSlot:
    id: int             # Identifiant unique (0, 1, 2...)
    direction: str      # 'H' (Horizontal) ou 'V' (Vertical)
    row: int            # Ligne de départ
    col: int            # Colonne de départ
    length: int         # Longueur du mot
    cells: List[Tuple[int, int]] # Liste des coordonnées (row, col) occupées

class GridStructure:
    def __init__(self, grid_layout: List[str]):
        """
        grid_layout: Liste de strings représentant la grille.
                     '#' = case noire, '.' = case blanche
        """
        self.grid = grid_layout
        self.rows = len(grid_layout)
        self.cols = len(grid_layout[0])
        
        self.slots = []           # Liste de tous les WordSlot
        self.intersections = []   # Liste des croisements
        
        # On lance l'analyse tout de suite
        self._parse_slots()
        self._find_intersections()

    def _parse_slots(self):
        """Détecte les mots horizontaux et verticaux."""
        slot_id = 0

        # 1. Analyse Horizontale
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                if self.grid[r][c] == '.': # Début potentiel d'un mot
                    start_col = c
                    length = 0
                    cells = []
                    while c < self.cols and self.grid[r][c] == '.':
                        cells.append((r, c))
                        length += 1
                        c += 1
                    
                    # On garde seulement les mots de longueur >= 2
                    if length >= 2:
                        slot = WordSlot(slot_id, 'H', r, start_col, length, cells)
                        self.slots.append(slot)
                        slot_id += 1
                else:
                    c += 1

        # 2. Analyse Verticale
        for c in range(self.cols):
            r = 0
            while r < self.rows:
                if self.grid[r][c] == '.':
                    start_row = r
                    length = 0
                    cells = []
                    while r < self.rows and self.grid[r][c] == '.':
                        cells.append((r, c))
                        length += 1
                        r += 1
                    
                    if length >= 2:
                        slot = WordSlot(slot_id, 'V', start_row, c, length, cells)
                        self.slots.append(slot)
                        slot_id += 1
                else:
                    r += 1

    def _find_intersections(self):
        """Trouve où les mots se croisent."""
        # On compare chaque slot Horizontal avec chaque slot Vertical
        horiz_slots = [s for s in self.slots if s.direction == 'H']
        vert_slots = [s for s in self.slots if s.direction == 'V']

        for h_slot in horiz_slots:
            for v_slot in vert_slots:
                # Vérifie s'ils partagent une cellule commune
                # (Intersection des ensembles de coordonnées)
                common_cells = set(h_slot.cells).intersection(set(v_slot.cells))
                
                if common_cells:
                    # Il y a croisement ! (Normalement un seul point)
                    coord = list(common_cells)[0]
                    
                    # À quel index (0, 1, 2...) de chaque mot se trouve le croisement ?
                    h_index = h_slot.cells.index(coord)
                    v_index = v_slot.cells.index(coord)
                    
                    self.intersections.append({
                        'id_h': h_slot.id,      # ID du mot horizontal
                        'id_v': v_slot.id,      # ID du mot vertical
                        'index_h': h_index,     # Index de la lettre dans le mot H
                        'index_v': v_index      # Index de la lettre dans le mot V
                    })

    def print_report(self):
        print(f"\n--- Analyse de la Grille {self.rows}x{self.cols} ---")
        print(f"Nombre de mots à trouver (Slots) : {len(self.slots)}")
        print(f"Nombre de croisements (Contraintes) : {len(self.intersections)}")
        
        print("\n--- Liste des Slots ---")
        for s in self.slots:
            print(f"ID {s.id} ({s.direction}) : Pos({s.row},{s.col}), Longueur {s.length}")
            
        print("\n--- Exemples de Croisements ---")
        for i, inter in enumerate(self.intersections[:5]): # Affiche les 5 premiers
            print(f"Le mot ID {inter['id_h']} (idx {inter['index_h']}) croise le mot ID {inter['id_v']} (idx {inter['index_v']})")

if __name__ == "__main__":
    # --- GÉNÉRATION D'UNE GRILLE ALÉATOIRE 12x12 ---
    ROWS, COLS = 10, 10
    NB_NOIRES = 15

    # 1. Création grille vide
    # On utilise une liste de listes pour pouvoir modifier facilement
    temp_grid = [['.' for _ in range(COLS)] for _ in range(ROWS)]

    # 2. Ajout des cases noires aléatoires
    count = 0
    while count < NB_NOIRES:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        if temp_grid[r][c] == '.':
            temp_grid[r][c] = '#'
            count += 1

    # Conversion en format attendu par GridStructure (liste de strings)
    grille_test = ["".join(row) for row in temp_grid]

    # 3. Affichage visuel (A-L, 1-12)
    print(f"\n--- Grille Générée ({ROWS}x{COLS} avec {NB_NOIRES} cases noires) ---")
    print("   " + " ".join([chr(65 + i) for i in range(COLS)])) # A B C ...
    for i, row in enumerate(grille_test):
        print(f"{str(i + 1).rjust(2)} {' '.join(list(row))}")

    print("\n--- Lancement de l'analyse ---")
    # On crée l'analyseur avec notre grille test
    analyseur = GridStructure(grille_test)
    # On affiche le résultat
    analyseur.print_report()