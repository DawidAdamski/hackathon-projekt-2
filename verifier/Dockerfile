# Używamy oficjalnego obrazu Pythona
FROM python:3.9-slim

# Instalujemy zależności
WORKDIR /verifier
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy kod aplikacji
COPY . .

# Uruchamiamy aplikację FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
