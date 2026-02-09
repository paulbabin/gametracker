#!/bin/bash
# Option 'set -e' : Arrête le script dès qu'une commande échoue 
set -e

echo "=================================================="
echo "      LANCEMENT DU PIPELINE GAMETRACKER"
echo "=================================================="

# 1. Attente de la base de données 
echo "[1/4] Verification de la disponibilite de la base de donnees..."
./scripts/wait-for-db.sh

# 2. Initialisation des tables 
echo "[2/4] Initialisation du schema SQL..."
# Utilisation des variables d'environnement du conteneur pour la connexion
mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --skip-ssl "$DB_NAME" < scripts/init-db.sql

# 3. Exécution du pipeline ETL Python 
# Note : Cela appellera le fichier main.py (que nous allons créer à l'étape 5)
echo "[3/4] Execution du pipeline ETL (Extract -> Transform -> Load)..."
python src/main.py

# 4. Génération du rapport 
echo "[4/4] Generation du rapport de synthese..."
# Appel direct de la fonction generate_report via une commande Python
python -c "from src.report import generate_report; generate_report()"

echo "=================================================="
echo "       PIPELINE TERMINE AVEC SUCCES"
echo "=================================================="