FROM node:18-alpine

WORKDIR /app

# Kopírování a instalace závislostí
COPY package.json package-lock.json ./
RUN npm install

# Kopírování aplikace
COPY . .

# Expozice portu a spuštění serveru
EXPOSE 3000
CMD ["npm", "start"]
