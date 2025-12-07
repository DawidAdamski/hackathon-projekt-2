from pydantic import BaseModel


class VerifySessionRequest(BaseModel):
    url: str
    service_id: str
