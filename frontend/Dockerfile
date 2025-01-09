# Указываем базовый образ
FROM node:20 AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все остальные файлы проекта
COPY . .

# Собираем приложение
RUN npm run build

# Создаем финальный образ
FROM node:20 AS production

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только необходимые файлы из сборки
COPY --from=builder /app/dist ./dist
COPY package*.json ./

# Устанавливаем только продакшн зависимости
RUN npm install --only=production

# Указываем команду для запуска приложения
CMD ["node", "dist/server.js"]