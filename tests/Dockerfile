# Dockerfile
FROM python:3.11-slim-buster

WORKDIR /app

COPY ./tests/requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./tests/RPi.GPIO.py ./sensor/RPi.GRIO.py

COPY . .

RUN ls -l

CMD ["pytest", "-vvs", "tests.py"]