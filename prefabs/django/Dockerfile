FROM python:3.10

WORKDIR /app
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt