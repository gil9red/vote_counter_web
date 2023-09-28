# vote_counter_web

---

# Переменные окружения

* DB_DIRECTORY_PATH - путь к папке, в которой будет храниться база данных SQLITE
* FLASK_RUN_PORT - порт сервера
* ALLOWED_IP_LIST - список через запятую для перечисления IP тех, у кого есть доступ для отмены чужих голосов
* ONLY_ALLOWED_IP_LIST_MAY_VOTE - при значении true, список из ALLOWED_IP_LIST еще ограничивает добавление голосов

# Docker
## Сборка образа
```
docker build -t vote_counter_web .
```
## Запуск контейнера
```
docker run --name vote_counter_web -p 0.0.0.0:11111:11111 vote_counter_web
```

Монтирование папки базы данных:
```
docker run --name vote_counter_web --mount "type=bind,src=.\database,target=/app-database" -p 0.0.0.0:11111:11111 vote_counter_web
```