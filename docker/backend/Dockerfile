FROM python:3.8.0-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend .

EXPOSE 8080

CMD [ "python", "main.py"]