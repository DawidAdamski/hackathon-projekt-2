from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Lista zaufanych domen
TRUSTED_DOMAINS = ["podatki.gov.local"]


# Model danych dla sesji weryfikacyjnej
class VerifySessionRequest(BaseModel):
    url: str
    service_id: str


# Endpoint do tworzenia sesji weryfikacyjnych
@app.post("/verify/session")
async def create_verify_session(request: VerifySessionRequest, req: Request):
    # Pobierz nagłówek Host
    host = req.headers.get("host")

    # Sprawdź, czy domena jest zaufana
    if host not in TRUSTED_DOMAINS:
        raise HTTPException(status_code=403, detail="Untrusted domain")

    # Generowanie sesji weryfikacyjnej (symulacja)
    nonce = "example_nonce"
    qr_payload = f"moby-sim://verify?nonce={nonce}"

    return {"nonce": nonce, "qr_payload": qr_payload}


# Endpoint do sprawdzania wyniku weryfikacji
@app.get("/verify/result")
async def get_verify_result(nonce: str):
    # Symulacja wyniku weryfikacji
    if nonce == "example_nonce":
        return {"status": "trusted"}
    else:
        return {"status": "untrusted"}


# Endpoint do sprawdzania wyniku weryfikacji
@app.get("/")
async def test_connection():
    return {"status": "verifier is running"}
