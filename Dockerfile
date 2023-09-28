# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

LABEL maintainer="https://github.com/gil9red"

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

ENV DB_DIRECTORY_PATH=/app-database
ENV FLASK_RUN_PORT=11111
EXPOSE $FLASK_RUN_PORT

ENTRYPOINT ["python3"]
CMD ["main.py"]
