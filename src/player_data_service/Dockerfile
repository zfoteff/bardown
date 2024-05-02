FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/player_data_service

WORKDIR /app/player_data_service

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 3001
CMD ["python", "-m", "player_data_service.py"]
