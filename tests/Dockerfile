# Dockerfile
FROM python:3.11-slim-buster

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["pytest", "-vvs", "tests.py"]