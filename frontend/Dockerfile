# Usa una imagen base de Node.js
FROM node:22.19.0-slim AS base

# Instala pnpm de manera global
RUN npm install -g pnpm

# Establece el directorio de trabajo
WORKDIR /app

# Usa una imagen base de Node.js
FROM base AS dev

WORKDIR /app
# Copia los archivos de configuración de paquetes
COPY package*.json .
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Cambia a un usuario no root
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  git \
  zsh \
  zsh-syntax-highlighting \
  zsh-autosuggestions \
  locate \
  lsd \
  bat \
  ssh \
  fzf \
  curl \
  wget \
  scrub && \
  rm -rf /var/lib/apt/lists/* && \
  chsh -s $(which zsh) node
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  docker.io && \
  rm -rf /var/lib/apt/lists/*
RUN groupmod -g 973 docker || true
RUN groupadd -f docker && usermod -aG docker node
RUN updatedb
RUN chsh -s $(which zsh) node || usermod --shell $(which zsh) node

USER node

ENV HOST=0.0.0.0
ENV PORT=3000


EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]
