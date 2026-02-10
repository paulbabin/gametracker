import pandas as pd

def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme et nettoie les donnees des joueurs.
    """
    df = df.copy()

    # 1. Supprimer les doublons sur player_id et username (on enleve les espaces d'abord)
    df['username'] = df['username'].str.strip()
    df = df.drop_duplicates(subset=['player_id'])
    df = df.drop_duplicates(subset=['username'], keep='first')

    # 2. Nettoyer les pseudos (strip)
    df['username'] = df['username'].str.strip()

    # 3. Convertir les dates d'inscription
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # Remplacer NaT par None pour MySQL
    df['registration_date'] = df['registration_date'].where(
        df['registration_date'].notna(), None
    )

    # 4. Nettoyer les emails invalides
    df['email'] = df['email'].where(
        df['email'].str.contains('@', na=False), None
    )

    print(f"Transforme {len(df)} joueurs")
    return df

def transform_scores(df: pd.DataFrame, valid_player_ids: list) -> pd.DataFrame:
    """
    Transforme et nettoie les donnees des scores.
    Args:
        df: DataFrame brut des scores.
        valid_player_ids: Liste des ID de joueurs valides.
    Returns:
        DataFrame nettoye.
    """
    df = df.copy()

    # 1. Supprimer les doublons sur score_id
    df = df.drop_duplicates(subset=['score_id'])

    # 2. Convertir les scores et durees en numerique
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')

    # On force la conversion en date. 'date_invalide' deviendra NaT (Not a Time)
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
    
    # On remplace les NaT par None (NULL SQL)
    df['played_at'] = df['played_at'].where(
        df['played_at'].notna(), None
    )
    # -----------------------------------------------------

    # 3. Filtrer les scores invalides (> 0)
    df = df[df['score'] > 0]

    # 4. Filtrer les scores orphelins
    df = df[df['player_id'].isin(valid_player_ids)]

    print(f"Transforme {len(df)} scores")
    return df