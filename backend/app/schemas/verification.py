from pydantic import BaseModel


class VerifySessionRequest(BaseModel):
    url: str
    service_id: str


class ScanRequest(BaseModel):
    nonce: str
    mobywatel: str = "mObywatel-mock"
