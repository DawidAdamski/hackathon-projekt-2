from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from services.storage import TokenStorage

from main import get_token_storage

router = APIRouter()

# Lista zaufanych domen
TRUSTED_DOMAINS = [
    "datki.gov",
    "podatki.gov",
    "wydatki.gov",
]


class VerifySessionRequest(BaseModel):
    url: str
    service_id: str


# Endpoint do tworzenia akcji weryfikacyjnych
@router.post("/session")
async def create_verify_session(
    request: VerifySessionRequest,
    req: Request,
    storage=Depends(get_token_storage),
):

    # CHECK 1: Czy w domenie .gov ?
    origin = req.headers.get("host", "")
    if origin.endswith(".gov") is False:
        raise HTTPException(status_code=403, detail="Domain is not .gov")

    # CHECK 2: Czy w zaufanych domenach?
    if origin not in TRUSTED_DOMAINS:
        raise HTTPException(status_code=403, detail=f"{req.headers.items()}")

    # Generowanie sesji weryfikacyjnej (symulacja)
    # 1. QRCOD nonce ma byc wygenerowany po stronie backednu
    import time
    from uuid import uuid4

    # 1 I NEED TO GENERATE NONCE TOKEN
    nonce = uuid4()
    SESSIONS[nonce] = {
        "status": "pending",
        "created_at": time.time(),
        "ttl": 30,  # sekund – to możesz ustawić dowolnie
        "url": url,
        "service_id": service_id,
    }

    # 2. Ma miec TTL
    # 3. Bacnekd ma miec informacje przez jaka strone zostal wygenerowny ten QRCode - dla jakiej domeny
    nonce = "example_nonce"
    qr_payload = f"moby-sim://verify?nonce={nonce}"
    # Kod QR generowany po stronie FrontEnd i jest graficzna reprezentacja stringa ktory zwracam mu z backendu

    # 4. Wysylasz ten QR code fo front serwera
    # i wyswietlasz w przegladace
    # 5. To ma zeskanowac user - zasymuluj to
    # 6. na potrzeby moka wysweitl do skopiowania kod
    #
    #

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
