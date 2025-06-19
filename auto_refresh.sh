#!/bin/bash

cd /home/lancelot/projects/statistic || { echo "Dossier non trouvé"; exit 1; }

# 2. Activer l'environnement virtuel
source .venv/bin/activate || { echo "Échec de l'activation de l'environnement virtuel"; exit 1; }

nohup python auto_refresh.py > auto_refresh.out 2>&1 &

deactivate
