#!/bin/bash
# entrypoint.sh

if grep -q "alias django=" ~/.zshrc 2>/dev/null; then
  sed -i '/alias django=/d' ~/.zshrc
fi
echo "alias django='python /app/src/manage.py'" >> ~/.zshrc


# Comprobar la existencia de requirements.txt en el directorio actual
if [ -f "./requirements.txt" ] && [ -d "./src" ]; then
  cd ./src
  python manage.py wait_for_db
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
else
  # Mantener el contenedor vivo si no hay `requirements.txt` o `src`
  echo "No se encontró el archivo requirements.txt o el directorio src. Esperando..."
  tail -f /dev/null
fi
