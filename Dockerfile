FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./
COPY requirements/ requirements/
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
