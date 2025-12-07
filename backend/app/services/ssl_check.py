import socket
import ssl
from datetime import datetime

# NOTE: FOR POC WE USE REAL DOMAIN WITH CERT TO GET DATA
# ONLY FOR POC
HARDCODED_DOMAIN = "gov.pl"


def get_cert_info(hostname: str, port: int = 443) -> dict | None:

    # NOTE: ONLY FOR POC
    hostname = HARDCODED_DOMAIN

    ctx = ssl.create_default_context()

    with socket.create_connection((hostname, port), timeout=5) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    if not cert:
        return None

    # SUBJECT
    subject_dict = dict(x[0] for x in cert.get("subject", []))
    cn = subject_dict.get("commonName")
    org = subject_dict.get("organizationName") or subject_dict.get("O")
    org_unit = subject_dict.get("organizationalUnitName") or subject_dict.get("OU")

    # ISSUER
    issuer_dict = dict(x[0] for x in cert.get("issuer", []))
    issuer_cn = issuer_dict.get("commonName")
    issuer_org = issuer_dict.get("organizationName") or issuer_dict.get("O")

    # SAN
    san_dns = [val for (t, val) in cert.get("subjectAltName", []) if t == "DNS"]

    not_before = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
    not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")

    return {
        "common_name": cn,
        "organization": org,
        "organizational_unit": org_unit,
        "issuer_common_name": issuer_cn,
        "issuer_organization": issuer_org,
        "san_dns": san_dns,
        "not_before": not_before,
        "not_after": not_after,
    }


if __name__ == "__main__":
    # przykład użycia
    info = get_cert_info("gov.pl")
    print(info["organization"], info["issuer_organization"])
