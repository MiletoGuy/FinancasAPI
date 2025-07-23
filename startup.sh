#!/bin/bash

LOG_FILE=/home/LogFiles/startup.log
echo "== Iniciando startup ==" >> $LOG_FILE
echo "Diretório atual: $(pwd)" >> $LOG_FILE
ls -l >> $LOG_FILE

# Caminho padrão da aplicação
APP_DIR=/home/site/wwwroot

# Extrair a aplicação se necessário
cd $APP_DIR
if [ -f output.tar.gz ]; then
    echo "== Extraindo output.tar.gz ==" >> $LOG_FILE
    tar -xzf output.tar.gz --exclude='antenv' --overwrite >> $LOG_FILE 2>&1
else
    echo "Arquivo output.tar.gz não encontrado" >> $LOG_FILE
fi

# Confirma se app.py está lá
ls -l $APP_DIR >> $LOG_FILE

# Rodar o Gunicorn de dentro do wwwroot
cd $APP_DIR
echo "== Iniciando Gunicorn ==" >> $LOG_FILE
gunicorn --bind=0.0.0.0:8000 app:app >> $LOG_FILE 2>&1