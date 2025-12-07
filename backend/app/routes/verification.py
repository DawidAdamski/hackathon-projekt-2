import re

from app.core.logger import logger
from app.schemas.verification import ScanRequest, VerifySessionRequest
from app.services.storage import TokenService, get_token_service
from app.services.token_generator import generate_nonce_token
from app.services.validator import is_gov_domain, is_trusted_domain
from fastapi import APIRouter, Depends, Request

router = APIRouter()


# Endpoint do tworzenia akcji weryfikacyjnych
@router.post("/session")
async def create_verify_session(
    request: VerifySessionRequest,
    req: Request,
    token_service: TokenService = Depends(get_token_service),
):
    origin = req.headers.get("host", "")
    is_gov_domain(origin)
    is_trusted_domain(origin)

    # NOTE: On backend we generate token - fornted will be responsible for creaing QR code
    # That represents the payload with the token

    nonce = generate_nonce_token()
    qr_payload = f"moby-sim://verify?nonce={nonce}"
    token_service.save_token(token=nonce, domain=origin)

    # NOTE: We return nonce token base on what QRCode will be generated on frontend
    # For mock purpouses the exact value is displayed for copy and paste in mock mObywatel app
    return {
        "nonce": nonce,
        "qr_payload": qr_payload,
    }


@router.get("/result")
async def get_verify_result(
    nonce: str,
    req: Request,
    token_service: TokenService = Depends(get_token_service),
):
    origin = req.headers.get("host", "")
    logger.info(f"Verifying nonce: {nonce} from origin: {origin}")

    token = token_service.load(nonce)
    logger.info(f"Loaded token data: {token}")

    if not token:
        return {"status": "untrusted"}

    if token["domain"] != origin:
        return {"status": "untrusted"}

    if not token["mobywatel_scan"]:
        return {"status": "waiting for scan"}

    else:
        token_service.remove(nonce)
        return {"status": "trusted"}


@router.post("/scan")
async def handle_scan(
    request: ScanRequest,
    req: Request,
    token_service: TokenService = Depends(get_token_service),
):
    """
    Endpoint wywoływany przez mObywatel po zeskanowaniu kodu QR.
    Aktualizuje flagę mobywatel_scan na 1.
    """
    nonce = request.nonce
    origin = req.headers.get("host", "")
    logger.info(f"Scan request for nonce: {nonce} from origin: {origin}, mobywatel: {request.mobywatel}")

    token = token_service.update(nonce)
    logger.info(f"Token after update: {token}")

    if not token:
        logger.warning(f"Token not found or expired: {nonce}")
        return {"status": "untrusted", "details": "Token nie został znaleziony lub wygasł"}
    else:
        return {"status": "trusted", "origin": token["domain"], "details": "Weryfikacja zakończona pomyślnie"}


@router.get("/test")
async def get_test():
    return {"status": "router ok"}
