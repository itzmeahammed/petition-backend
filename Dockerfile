FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

COPY .env .env

RUN pip install --upgrade pip

# RUN apt-get update && apt-get install -y git

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6777


CMD ["python","app.py"]