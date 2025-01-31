# Используем официальный образ Node.js
FROM node:20 AS build

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь код приложения
COPY . .

RUN npm run build

# Используем Nginx для раздачи статики
FROM nginx:alpine

# Удаляем дефолтные настройки
RUN rm /etc/nginx/conf.d/default.conf

# Копируем статические файлы React
COPY --from=build /app/dist /usr/share/nginx/html

# replace with custom one
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf
# --------- /only for those using react router ----------
# expose port 80 to the outer world
EXPOSE 3000
# start nginx
CMD ["nginx", "-g", "daemon off;"]

