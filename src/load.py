import pandas as pd

def load_players(df: pd.DataFrame, conn) -> int:
    """
    Charge les joueurs dans la base de donnees.
    Args:
        df: DataFrame des joueurs.
        conn: Connexion MySQL.
    Returns:
        Nombre de lignes inserees.
    """
    cursor = conn.cursor()
    # On utilise ON DUPLICATE KEY UPDATE pour gérer les mises à jour
    query = """
    INSERT INTO players
    (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        registration_date = VALUES(registration_date),
        country = VALUES(country),
        level = VALUES(level)
    """
    
    count = 0
    # On itère ligne par ligne comme dans le cours
    for _, row in df.iterrows():
        values = (
            int(row['player_id']),
            row['username'],
            # Gestion explicite des NULL pour l'email
            row['email'] if pd.notna(row['email']) else None,
            # Formatage de la date YYYY-MM-DD
            row['registration_date'].strftime('%Y-%m-%d') 
            if pd.notna(row['registration_date']) else None,
            row['country'],
            int(row['level'])
        )
        cursor.execute(query, values)
        count += 1
    
    # Important : on valide la transaction à la fin
    conn.commit()
    print(f"Charge {count} joueurs")
    return count

def load_scores(df: pd.DataFrame, conn) -> int:
    """
    Charge les scores dans la base de donnees.
    Args:
        df: DataFrame des scores.
        conn: Connexion MySQL.
    Returns:
        Nombre de lignes inserees.
    """
    cursor = conn.cursor()
    query = """
    INSERT INTO scores
    (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        player_id = VALUES(player_id),
        game = VALUES(game),
        score = VALUES(score),
        duration_minutes = VALUES(duration_minutes),
        played_at = VALUES(played_at),
        platform = VALUES(platform)
    """
    
    count = 0
    for _, row in df.iterrows():
        values = (
            row['score_id'],
            int(row['player_id']),
            row['game'],
            # Conversion explicite en int/float pour éviter les soucis numpy
            int(row['score']) if pd.notna(row['score']) else 0,
            int(row['duration_minutes']) if pd.notna(row['duration_minutes']) else 0,
            # Formatage de la date avec l'heure YYYY-MM-DD HH:MM:SS
            row['played_at'] if pd.notna(row['played_at']) else None, 
            # Note: Si played_at est déjà une string propre dans le CSV, on la laisse.
            # Si c'était un objet datetime, on ferait .strftime('%Y-%m-%d %H:%M:%S')
            row['platform']
        )
        cursor.execute(query, values)
        count += 1
        
    conn.commit()
    print(f"Charge {count} scores")
    return count