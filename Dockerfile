FROM python:latest


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY MyApp /app/MyApp

EXPOSE 8501

CMD [ "streamlit", "run", "/app/MyApp/ui.py", "--server.port=8501", "--server.address=0.0.0.0" ]