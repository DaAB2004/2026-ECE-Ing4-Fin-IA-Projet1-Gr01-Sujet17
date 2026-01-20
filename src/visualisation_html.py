import os
import random
import webbrowser
from grid_structure import GridStructure

# --- CONFIGURATION ---
ROWS = 10
COLS = 10
NB_NOIRES = 15
NOM_FICHIER_HTML = "grille_mots_croises.html"

def generer_grille_donnees():
    """Génère la matrice de la grille (liste de listes)."""
    grid = [['.' for _ in range(COLS)] for _ in range(ROWS)]
    count = 0
    while count < NB_NOIRES:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        if grid[r][c] == '.':
            grid[r][c] = '#'
            count += 1
    return grid

def creer_html(grid_data, analyseur):
    """Construit le code HTML pour afficher la grille et les infos."""
    
    # Début du HTML avec du CSS pour faire joli
    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Grille Mots Croisés IA</title>
        <style>
            body { font-family: sans-serif; background-color: #f4f4f9; padding: 20px; }
            h1 { color: #333; }
            .container { display: flex; gap: 40px; }
            
            /* Style de la grille */
            table { border-collapse: collapse; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            td { 
                width: 40px; height: 40px; 
                border: 1px solid #333; 
                text-align: center; font-size: 20px; font-weight: bold;
            }
            .header { background-color: #ddd; font-weight: bold; color: #555; border: none; }
            .black-cell { background-color: black; }
            .white-cell { background-color: white; }
            
            /* Style des infos */
            .info-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 400px; }
            ul { max-height: 400px; overflow-y: auto; }
            li { margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Générateur de Grille (10x10)</h1>
        <div class="container">
            <div>
                <table>
    """

    # 1. En-têtes de colonnes (A, B, C...)
    html += "<tr><td class='header'></td>"
    for c in range(COLS):
        html += f"<td class='header'>{chr(65 + c)}</td>"
    html += "</tr>"

    # 2. Lignes de la grille
    for r in range(ROWS):
        html += "<tr>"
        # En-tête de ligne (1, 2, 3...)
        html += f"<td class='header'>{r + 1}</td>"
        for c in range(COLS):
            css_class = "black-cell" if grid_data[r][c] == '#' else "white-cell"
            html += f"<td class='{css_class}'></td>"
        html += "</tr>"
    html += "</table></div>"

    # 3. Panneau d'informations (Analyse)
    html += f"""
            <div class="info-box">
                <h2>Analyse</h2>
                <p><strong>Mots à trouver :</strong> {len(analyseur.slots)}</p>
                <p><strong>Croisements :</strong> {len(analyseur.intersections)}</p>
                <h3>Détails des emplacements :</h3>
                <ul>
    """
    for s in analyseur.slots:
        coord = f"{chr(65 + s.col)}{s.row + 1}" # Ex: A1, B3
        direction = "Horizontal" if s.direction == 'H' else "Vertical"
        html += f"<li><strong>ID {s.id}</strong> ({direction}) : Début en {coord}, Longueur {s.length}</li>"
    
    html += """
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # Génération et Analyse
    grille = generer_grille_donnees()
    grille_str = ["".join(row) for row in grille] # Conversion pour l'analyseur
    analyseur = GridStructure(grille_str)

    # Création du HTML
    contenu_html = creer_html(grille, analyseur)
    
    # Sauvegarde et Ouverture
    chemin_html = os.path.join(os.path.dirname(__file__), NOM_FICHIER_HTML)
    with open(chemin_html, "w", encoding="utf-8") as f:
        f.write(contenu_html)
    
    print(f"Fichier HTML généré : {chemin_html}")
    webbrowser.open(chemin_html)