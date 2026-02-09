import os
import pandas as pd

def extract(filepath):
    """
    Lit un fichier CSV et retourne un DataFrame Pandas.
    Vérifie l'existence du fichier et affiche le nombre de lignes.
    """
    # 1. Vérifier l'existence du fichier
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Erreur : Le fichier '{filepath}' est introuvable.")
    
    try:
        # 2. Lire le CSV avec Pandas
        df = pd.read_csv(filepath)
        
        # 3. Afficher le nombre de lignes extraites
        print(f"--> Extraction reussie : {len(df)} lignes lues depuis {os.path.basename(filepath)}")
        
        return df
        
    except Exception as e:
        print(f"Erreur critique lors de la lecture de {filepath}: {e}")
        raise