# vote_counter_web

---

# Переменные окружения

* DB_DIRECTORY_PATH - путь к папке, в которой будет храниться база данных SQLITE
* FLASK_RUN_PORT - порт сервера
* FLASK_SECRET_KEY - секретный ключ сервера, используется для (рас)шифрования куков
* ADMIN_LOGIN - логин. По-умолчанию, admin
* ADMIN_PASSWORD - пароль. По-умолчанию, admin

# Docker
## Сборка образа
```
docker build --tag vote_counter_web .
```
## Запуск контейнера
```
docker run --name vote_counter_web --publish 0.0.0.0:11111:11111 vote_counter_web
```

Монтирование папки базы данных:
```
docker run --name vote_counter_web --mount "type=bind,src=.\database,target=/app-database" --publish 0.0.0.0:11111:11111 vote_counter_web
```

Установка логина и пароля через переменную окружения:
```
docker run --name vote_counter_web --env ADMIN_LOGIN="ADMIN" --env ADMIN_PASSWORD="IDDQD" --publish 0.0.0.0:11111:11111 vote_counter_web
```