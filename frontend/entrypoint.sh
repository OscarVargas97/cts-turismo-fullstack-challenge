#!/bin/bash
# entrypoint.sh

# Salir si algún comando falla

# Verifica si el directorio ./src existe y accede a él, si no, permanece en el directorio actual
# Verifica si package.json existe para instalar dependencias y arrancar el servidor
if [ -f "/app/package.json" ]; then
  echo "Instalando dependencias..."
  pnpm install

  echo "Iniciando servidor de desarrollo..."
  pnpm run dev

else
  echo "Archivo package.json no encontrado, no se instalarán dependencias ni se iniciará el servidor."
fi

# Mantiene el contenedor en ejecución
tail -f /dev/null
