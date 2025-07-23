#!/bin/bash

echo "== Iniciando startup ==" >> /home/LogFiles/startup.log

# Mostra o diretório atual
echo "Diretório atual: $(pwd)" >> /home/LogFiles/startup.log

# Lista os arquivos no diretório
echo "Conteúdo do diretório:" >> /home/LogFiles/startup.log
ls -l >> /home/LogFiles/startup.log

# Lista o wwwroot (caso esteja fora dele)
echo "Conteúdo do /home/site/wwwroot:" >> /home/LogFiles/startup.log
ls -l /home/site/wwwroot >> /home/LogFiles/startup.log

# Troca para o diretório correto
cd /home/site/wwwroot

# Mostra de novo o local após o cd
echo "Diretório após cd: $(pwd)" >> /home/LogFiles/startup.log
ls -l >> /home/LogFiles/startup.log

echo "== Iniciando Gunicorn ==" >> /home/LogFiles/startup.log

# Rodar a aplicação
gunicorn --bind=0.0.0.0:8000 app:app >> /home/LogFiles/startup.log 2>&1