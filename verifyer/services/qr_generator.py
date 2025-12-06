import base64
from io import BytesIO

import qrcode


def generate_qr_code(data: str):
    # Tworzenie obiektu QRCode
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    # Generowanie obrazu QR
    img = qr.make_image(fill="black", back_color="white")

    # Konwersja obrazu na Base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Zwracanie obrazu w Base64 i tekstu
    return {"qr_image": f"data:image/png;base64,{qr_base64}", "qr_text": data}


def generate_token():
    import uuid

    return uuid.uuid4().hex
