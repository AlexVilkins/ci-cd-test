# Используем официальный образ Node.js
FROM node:20-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь код приложения
COPY . .

RUN npm run build

EXPOSE 5173

# Запускаем приложение в режиме разработки
CMD ["npm", "run", "dev"]

