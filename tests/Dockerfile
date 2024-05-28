# Dockerfile
FROM python:3.11-slim-buster

WORKDIR /app

COPY ./tests/requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./tests/RPi.GPIO.py ./RPi.GPIO.py
COPY ./tests/RPi.GPIO.py ./sensor/RPi.GPIO.py

ENV PYTHONPATH /app:$PYTHONPATH

COPY . .

RUN ls -lAR

CMD ["pytest", "-vvs", "tests.py"]