echo "===== Iniciando startup.sh ====="

gunicorn --bind=0.0.0.0:$PORT --timeout=600 app:app

echo "===== Gunicorn foi chamado ====="
