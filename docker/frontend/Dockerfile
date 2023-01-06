FROM python:3.8.0-slim

WORKDIR /app

COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend .

EXPOSE 8501

CMD [ "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]