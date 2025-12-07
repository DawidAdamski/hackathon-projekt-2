from app.schemas.verification import VerifySessionRequest
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
    return {
        "nonce": nonce,
        "qr_payload": qr_payload,
    }

    # NOTE: We return nonce token base on what QRCode will be generated on frontend
    # For mock purpouses the exact value is displayed for copy and paste in mock mObywatel app

    # 5. To ma zeskanowac user - zasymuluj to przez dodanie input boxa na fronie mocka mobywatela ktory wysle request do
    #    dokonczenia veryfikacji
    # 6. na potrzeby moka wysweitl do skopiowania kod


# Endpoint do sprawdzania wyniku weryfikacji
@router.get("/result")
async def get_verify_result(nonce: str):
    # Symulacja wyniku weryfikacji
    if nonce == "example_nonce":
        return {"status": "trusted"}
    else:
        return {"status": "untrusted"}


@router.get("/scan")
async def handle_scan():
    return {"status": "router ok"}


@router.get("/test")
async def get_test():
    return {"status": "router ok"}
