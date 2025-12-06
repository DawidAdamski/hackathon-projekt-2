from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()

# Lista zaufanych domen
TRUSTED_DOMAINS = ["podatki.gov.local"]


# Model danych dla sesji weryfikacyjnej
class VerifySessionRequest(BaseModel):
    url: str
    service_id: str


# Endpoint do tworzenia akcji weryfikacyjnych
@router.post("/session")
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
@router.get("/result")
async def get_verify_result(nonce: str):
    # Symulacja wyniku weryfikacji
    if nonce == "example_nonce":
        return {"status": "trusted"}
    else:
        return {"status": "untrusted"}


@router.get("/test")
async def get_test():
    return {"status": "router ok"}
