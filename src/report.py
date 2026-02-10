import sys
import os
import datetime

def generate_report(conn):
    """
    Genere le rapport de synthese a partir des donnees en base.
    Args:
        conn: Objet de connexion MySQL (passe depuis le main)
    """
    print("Generation du rapport vers output/rapport.txt...")
    
    try:
        # On utilise le curseur de la connexion existante
        cursor = conn.cursor()
        
        # --- 1. REQUETES SQL ---
        
        # Stats generales
        cursor.execute("SELECT COUNT(*) FROM players")
        nb_players = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scores")
        nb_scores = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT game) FROM scores")
        nb_games = cursor.fetchone()[0]
        
        # Top 5
        cursor.execute("""
            SELECT p.username, s.game, s.score 
            FROM scores s 
            JOIN players p ON s.player_id = p.player_id 
            ORDER BY s.score DESC 
            LIMIT 5
        """)
        top_5 = cursor.fetchall()
        
        # Moyennes
        cursor.execute("SELECT game, AVG(score) FROM scores GROUP BY game")
        avg_scores = cursor.fetchall()
        
        # Pays
        cursor.execute("SELECT country, COUNT(*) FROM players GROUP BY country ORDER BY COUNT(*) DESC")
        players_by_country = cursor.fetchall()
        
        # Plateformes
        cursor.execute("SELECT platform, COUNT(*) FROM scores GROUP BY platform")
        platforms = cursor.fetchall()
        
        # --- 2. ECRITURE DU FICHIER ---
        
        with open('output/rapport.txt', 'w') as f:
            f.write("====================================================\n")
            f.write("GAMETRACKER - Rapport de synthese\n")
            f.write(f"Genere le : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("====================================================\n")
            
            f.write("--- Statistiques generales ---\n")
            f.write(f"Nombre de joueurs : {nb_players}\n")
            f.write(f"Nombre de scores : {nb_scores}\n")
            f.write(f"Nombre de jeux : {nb_games}\n")
            
            f.write("--- Top 5 des meilleurs scores ---\n")
            for i, (user, game, score) in enumerate(top_5, 1):
                f.write(f"{i}. {user} | {game} | {score}\n")
                
            f.write("--- Score moyen par jeu ---\n")
            for game, avg in avg_scores:
                f.write(f"{game} : {avg:.1f}\n")
                
            f.write("--- Joueurs par pays ---\n")
            for country, count in players_by_country:
                f.write(f"{country} : {count}\n")
                
            f.write("--- Sessions par plateforme ---\n")
            for plat, count in platforms:
                f.write(f"{plat} : {count}\n")
                
            f.write("====================================================\n")
            
        print("--> Rapport genere avec succes.")
        
    except Exception as e:
        print(f"Erreur lors de la generation du rapport : {e}")
        raise # On fait remonter l'erreur pour arrêter le pipeline si besoin