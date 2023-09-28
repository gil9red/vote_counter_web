# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

ENV FLASK_RUN_PORT=11111
EXPOSE 11111

ENTRYPOINT ["python3"]
CMD ["main.py"]
