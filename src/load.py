import pandas as pd

def load_players(df, conn):
    """
    Charge les données des joueurs dans la table 'players'.
    Gère les doublons via ON DUPLICATE KEY UPDATE.
    """
    if df.empty:
        print("Aucun joueur a charger.")
        return

    print(f"Chargement de {len(df)} joueurs...")
    cursor = conn.cursor()

    # Conversion des NaN/NaT pandas en None (NULL SQL) 
    df = df.where(pd.notnull(df), None)

    query = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        registration_date = VALUES(registration_date),
        country = VALUES(country),
        level = VALUES(level);
    """

    # Préparation des données pour l'insertion
    data = []
    for _, row in df.iterrows():
        data.append((
            row['player_id'],
            row['username'],
            row['email'],
            row['registration_date'],
            row['country'],
            row['level']
        ))

    try:
        cursor.executemany(query, data)
        conn.commit()
        print(f"--> Succes : {cursor.rowcount} lignes affectees (players).")
    except Exception as e:
        print(f"Erreur lors du chargement des joueurs : {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()


def load_scores(df, conn):
    """
    Charge les données des scores dans la table 'scores'.
    Gère les doublons via ON DUPLICATE KEY UPDATE.
    """
    if df.empty:
        print("Aucun score a charger.")
        return

    print(f"Chargement de {len(df)} scores...")
    cursor = conn.cursor()

    # Conversion des NaN/NaT pandas en None (NULL SQL) 
    df = df.where(pd.notnull(df), None)

    query = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        player_id = VALUES(player_id),
        game = VALUES(game),
        score = VALUES(score),
        duration_minutes = VALUES(duration_minutes),
        played_at = VALUES(played_at),
        platform = VALUES(platform);
    """

    data = []
    for _, row in df.iterrows():
        data.append((
            row['score_id'],
            row['player_id'],
            row['game'],
            row['score'],
            row['duration_minutes'],
            row['played_at'],
            row['platform']
        ))

    try:
        cursor.executemany(query, data)
        conn.commit()
        print(f"--> Succes : {cursor.rowcount} lignes affectees (scores).")
    except Exception as e:
        print(f"Erreur lors du chargement des scores : {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()