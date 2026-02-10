# GameTracker

## Description
GameTracker est un pipeline ETL (Extract, Transform, Load) automatisé conçu pour traiter des données de jeux vidéo. 
Le projet extrait des données brutes (CSV) concernant des joueurs et des scores, les nettoie pour garantir la qualité des données, les charge dans une base de données MySQL, et génère un rapport de synthèse statistique.

## Prérequis techniques
Pour lancer ce projet, vous avez besoin de :
- **Docker** et **Docker Compose** installés sur votre machine.
- **Git** (pour cloner le projet).
- Les fichiers sources `Players.csv` et `Scores.csv` dans le dossier `data/`.

## Instructions de lancement

1. **Démarrer l'environnement (Conteneurs)**
   Construit l'image Python et lance la base de données MySQL.
   ```bash
   docker compose up --build


2.  **Exécuter le Pipeline complet**
    Lance le script d'automatisation qui gère l'attente de la BDD, l'initialisation SQL, l'ETL Python et le rapport.
    ```bash
    docker compose exec app ./scripts/run_pipeline.sh
    ```

3.  **Consulter le résultat**
    Le rapport généré se trouve ici : `output/rapport.txt`.

4.  **Arrêter les services**
    ```bash
    docker compose down
    ```


## Structure du projet

Voici l'organisation des fichiers et leur rôle :

```text
gametracker/
├── data/                  # Données brutes (Entrée)
│   ├── Players.csv        # Fichier source des joueurs
│   └── Scores.csv         # Fichier source des scores
│
├── output/                # Données générées (Sortie)
│   └── rapport.txt        # Rapport de synthèse statistique
│
├── scripts/               # Scripts d'automatisation et SQL
│   ├── init-db.sql        # Création des tables (DDL)
│   ├── run_pipeline.sh    # Script principal : orchestre tout le flux
│   └── wait-for-db.sh     # Script d'attente de disponibilité MySQL
│
├── src/                   # Code source de l'application Python
│   ├── config.py          # Configuration via variables d'environnement
│   ├── database.py        # Gestion de la connexion MySQL (Retry logic)
│   ├── extract.py         # Lecture et validation des fichiers CSV
│   ├── transform.py       # Logique de nettoyage métier
│   ├── load.py            # Insertion en base (Upsert)
│   ├── report.py          # Génération du rapport texte
│   └── main.py            # Point d'entrée du programme ETL
│
├── docker-compose.yml     # Orchestration des conteneurs (App + DB)
├── Dockerfile             # Définition de l'image Python
├── requirements.txt       # Liste des dépendances Python
└── README.md              # Documentation du projet

```
## Problèmes de qualité traités
Le pipeline corrige automatiquement les anomalies suivantes avant l'insertion en base de données :

1. Nettoyage des Joueurs (transform_players)
Doublons : Suppression des lignes dupliquées basées sur l'identifiant unique player_id.

Formatage Texte : Suppression des espaces superflus (début/fin) dans les username.

Dates invalides : Conversion des dates d'inscription (registration_date). Les formats invalides sont convertis en NULL (NaT).

Emails invalides : Vérification de la présence du caractère @. Les emails non conformes sont remplacés par NULL.

2. Nettoyage des Scores (transform_scores)
Intégrité Référentielle (Orphelins) : Suppression des scores faisant référence à un player_id qui n'existe pas dans la liste des joueurs validés.

Valeurs Aberrantes : Suppression des scores négatifs ou nuls.

Doublons : Suppression des doublons basés sur score_id.

Typage des données : Conversion stricte des scores et durées en format numérique (int/float).