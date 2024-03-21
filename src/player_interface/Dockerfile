FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /player-interface

COPY ../src .
COPY ../requirements.txt .

RUN apt-get update -y \
    && apt-get upgrade -y \
    && mkdir ./logs/ \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 3000
CMD [""]
