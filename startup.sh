#!/bin/bash

echo "== Iniciando startup ==" >> /home/LogFiles/startup.log
cd /home/site/wwwroot

# Ativar ambiente virtual se necessário
if [ -d antenv ]; then
    echo "== Ativando venv ==" >> /home/LogFiles/startup.log
    source antenv/bin/activate
fi

# Rodar a aplicação com Gunicorn
echo "== Iniciando Gunicorn ==" >> /home/LogFiles/startup.log
gunicorn --bind=0.0.0.0:8000 app:app >> /home/LogFiles/startup.log 2>&1
