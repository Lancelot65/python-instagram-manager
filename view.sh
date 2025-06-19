#!/bin/bash

cd /home/lancelot/projects/statistic || { echo "Dossier non trouvé"; exit 1; }

# 2. Activer l'environnement virtuel
source .venv/bin/activate || { echo "Échec de l'activation de l'environnement virtuel"; exit 1; }

export FLASK_APP=flaskr
flask run --host=0.0.0.0 --port=8000 

deactivate
