import pandas as pd

def transform_players(df):
    """
    Nettoie les données des joueurs :
    1. Supprime les doublons (player_id)
    2. Nettoie les espaces (username)
    3. Convertit les dates (registration_date)
    4. Valide les emails
    """
    print("--- Transformation des joueurs ---")
    
    # 1. Supprimer les doublons sur player_id 
    nb_avant = len(df)
    df = df.drop_duplicates(subset=['player_id'], keep='first')
    print(f"Doublons supprimes : {nb_avant - len(df)}")

    # 2. Nettoyer les espaces des username (strip) 
    df['username'] = df['username'].str.strip()

    # 3. Convertir les dates d'inscription 
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')

    # 4. Remplacer les emails invalides (sans @) par None 
    # On applique une fonction lambda : si pas de '@', on met None
    def clean_email(email):
        if pd.isna(email) or '@' not in str(email):
            return None
        return email
    
    df['email'] = df['email'].apply(clean_email)
    
    print(f"Joueurs valides apres nettoyage : {len(df)}")
    return df


def transform_scores(df, valid_player_ids):
    """
    Nettoie les scores et vérifie la cohérence avec les joueurs :
    1. Supprime les doublons (score_id)
    2. Convertit les types (dates, scores)
    3. Supprime les scores négatifs
    4. Supprime les références orphelines (player_id inconnu)
    """
    print("--- Transformation des scores ---")
    
    # 1. Supprimer les doublons sur score_id 
    nb_avant = len(df)
    df = df.drop_duplicates(subset=['score_id'], keep='first')
    print(f"Doublons scores supprimes : {nb_avant - len(df)}")

    # 2. Convertir les types numériques et dates 
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')

    # 3. Supprimer les lignes avec un score négatif ou nul (et les NaN issus de la conversion) 
    nb_avant_score = len(df)
    df = df[df['score'] > 0]
    print(f"Scores invalides (<=0 ou NaN) supprimes : {nb_avant_score - len(df)}")

    # 4. Supprimer les scores dont le player_id n'est pas dans valid_player_ids 
    nb_avant_orphans = len(df)
    # On ne garde que les lignes où le player_id est dans la liste des IDs valides
    df = df[df['player_id'].isin(valid_player_ids)]
    print(f"Scores orphelins supprimes : {nb_avant_orphans - len(df)}")

    print(f"Scores valides apres nettoyage : {len(df)}")
    return df