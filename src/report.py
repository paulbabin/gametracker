import os
from datetime import datetime
from src.database import database_connection

def generate_report():
    """
    Génère un rapport de synthèse dans output/rapport.txt
    en interrogeant la base de données.
    """
    output_path = "output/rapport.txt"
    print(f"Generation du rapport vers {output_path}...")
    
    try:
        # On utilise le context manager créé à l'étape 2 
        with database_connection() as conn:
            cursor = conn.cursor()
            
            # Liste pour stocker les lignes du rapport avant écriture
            lines = []
            
            # --- EN-TÊTE ---
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lines.append("====================================================")
            lines.append("GAMETRACKER - Rapport de synthese")
            lines.append(f"Genere le : {now}")
            lines.append("====================================================")
            
            # --- 1. STATISTIQUES GÉNÉRALES ---
            lines.append("--- Statistiques generales ---")
            
            cursor.execute("SELECT COUNT(*) FROM players")
            nb_players = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM scores")
            nb_scores = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT game) FROM scores")
            nb_games = cursor.fetchone()[0]
            
            lines.append(f"Nombre de joueurs : {nb_players}")
            lines.append(f"Nombre de scores : {nb_scores}")
            lines.append(f"Nombre de jeux : {nb_games}")
            
            # --- 2. TOP 5 DES MEILLEURS SCORES ---
            # Utilisation de JOIN et ORDER BY
            lines.append("--- Top 5 des meilleurs scores ---")
            query_top = """
                SELECT p.username, s.game, s.score 
                FROM scores s 
                JOIN players p ON s.player_id = p.player_id 
                ORDER BY s.score DESC 
                LIMIT 5
            """
            cursor.execute(query_top)
            # enumerate(..., 1) permet de commencer la numérotation à 1
            for rank, (user, game, score) in enumerate(cursor.fetchall(), 1):
                lines.append(f"{rank}. {user} | {game} | {score}")

            # --- 3. SCORE MOYEN PAR JEU ---
            # Utilisation de AVG et GROUP BY
            lines.append("--- Score moyen par jeu ---")
            cursor.execute("SELECT game, AVG(score) FROM scores GROUP BY game")
            for game, avg in cursor.fetchall():
                lines.append(f"{game} : {avg:.1f}")

            # --- 4. JOUEURS PAR PAYS ---
            lines.append("--- Joueurs par pays ---")
            cursor.execute("SELECT country, COUNT(*) FROM players GROUP BY country ORDER BY COUNT(*) DESC")
            for country, count in cursor.fetchall():
                lines.append(f"{country} : {count}")

            # --- 5. SESSIONS PAR PLATEFORME ---
            lines.append("--- Sessions par plateforme ---")
            cursor.execute("SELECT platform, COUNT(*) FROM scores GROUP BY platform ORDER BY COUNT(*) DESC")
            for platform, count in cursor.fetchall():
                lines.append(f"{platform} : {count}")
            
            lines.append("====================================================")

            # Écriture dans le fichier 
            # On s'assure que le dossier output existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
                
            print(f"--> Rapport genere avec succes.")

    except Exception as e:
        print(f"Erreur lors de la generation du rapport : {e}")
        raise