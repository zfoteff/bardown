FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/player_interface

WORKDIR /app/player_interface

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 3000
CMD ["python", "-m", "player_interface.py"]
