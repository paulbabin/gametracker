#!/bin/bash
# Script d'automatisation du pipeline ETL

# Configuration de la base de donnees
DB_HOST="db"
DB_PORT="3306"
DB_USER="root"
DB_PASSWORD="root" # A adapter selon ton docker-compose
DB_NAME="etl_db"

echo "=================================================="
echo "      LANCEMENT DU PIPELINE GAMETRACKER"
echo "=================================================="

# Etape 1 : Attente de la BDD
echo "[1/4] Verification de la disponibilite de la base de donnees..."
./scripts/wait-for-db.sh
if [ $? -ne 0 ]; then
    echo "Erreur : La base de donnees n'est pas accessible."
    exit 1
fi
echo "Base de donnees prete!"

# Etape 2 : Initialisation SQL
echo "[2/4] Initialisation du schema SQL..."
mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --skip-ssl "$DB_NAME" < scripts/init-db.sql
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'initialisation SQL."
    exit 1
fi

# Etape 3 : Execution du code Python (ETL + Rapport)
echo "[3/4] Execution du pipeline ETL (Extract -> Transform -> Load + Rapport)..."
python src/main.py
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'execution du script Python."
    exit 1
fi

# Etape 4 : Validation
echo "[4/4] Verification finale..."
if [ -f "output/rapport.txt" ]; then
    echo "Rapport trouve : output/rapport.txt"
else
    echo "Attention : Le fichier rapport.txt n'a pas ete trouve."
fi

echo "=================================================="
echo "       PIPELINE TERMINE AVEC SUCCES"
echo "=================================================="