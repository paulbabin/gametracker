"""
Point d'entree du pipeline ETL.
"""
import os
import sys

# Ajout au path pour garantir les imports dans Docker
sys.path.append(os.getcwd())

from src.config import Config
from src.database import database_connection
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.report import generate_report

def run_pipeline():
    """ Execute le pipeline ETL complet. """
    print("=" * 50)
    print("Demarrage du pipeline ETL")
    print("=" * 50)

    with database_connection() as conn:
        # ETL Players (Joueurs)
        print("\n--- Traitement des Joueurs ---")
        # On utilise os.path.join pour la compatibilité, mais c'est l'esprit du f-string du prof
        players_path = os.path.join(Config.DATA_DIR, 'Players.csv')
        
        df_players = extract(players_path)
        df_players = transform_players(df_players)
        load_players(df_players, conn)

        # Spécifique GameTracker : On récupère les IDs valides pour l'étape suivante
        valid_player_ids = df_players['player_id'].tolist()

        # ETL Scores
        print("\n--- Traitement des Scores ---")
        scores_path = os.path.join(Config.DATA_DIR, 'Scores.csv')
        
        df_scores = extract(scores_path)
        # On passe la liste des IDs valides pour filtrer les orphelins
        df_scores = transform_scores(df_scores, valid_player_ids)
        load_scores(df_scores, conn)

        # Génération du rapport (Demandé dans ton sujet)
        print("\n--- Generation du Rapport ---")
        generate_report(conn)

    print("\n" + "=" * 50)
    print("Pipeline termine avec succes !")
    print("=" * 50)

if __name__ == '__main__':
    run_pipeline()