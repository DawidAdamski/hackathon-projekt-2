import base64
import os
from uuid import uuid4


def generate_nonce_token():

    # NOTE: Sposob generowania tokena mozna przerobic
    # random_bytes = os.urandom(length)
    # nonce_token = base64.urlsafe_b64encode(random_bytes).rstrip(b"=").decode("utf-8")

    nonce_token = uuid4()
    return nonce_token
