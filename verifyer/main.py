from fastapi import FastAPI
from routes.verifyer import router as verification_router

app = FastAPI()

app.include_router(verification_router, prefix="/verify")


# Endpoint do sprawdzania wyniku weryfikacji
@app.get("/")
async def test_connection():
    return {"status": "verifyer is running"}
