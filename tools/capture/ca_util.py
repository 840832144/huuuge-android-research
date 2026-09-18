#!/usr/bin/env python3
"""Android certificate-store helpers shared by the capture tooling."""
from __future__ import annotations

import base64
import hashlib
import pathlib
import re
import struct


def android_cert_hash(pem_path) -> str:
    """Return the file name Android expects for a CA in /system/etc/security/cacerts.

    That name is OpenSSL's ``subject_hash_old`` of the certificate subject, hex,
    with an ``.0`` suffix (e.g. ``b69ec367.0``). Computing it beats hardcoding it,
    because it changes with every CA you generate.
    """
    try:
        from cryptography import x509
    except Exception:
        raise SystemExit("需要 cryptography 来计算证书文件名：pip install cryptography")

    pem = pathlib.Path(pem_path).read_bytes()
    m = re.search(rb"-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----", pem, re.S)
    if not m:
        raise SystemExit("{} 不是 PEM 证书".format(pem_path))
    der = base64.b64decode(m.group(1).strip())
    cert = x509.load_der_x509_certificate(der)
    digest = hashlib.sha1(cert.subject.public_bytes()).digest()
    return "%08x.0" % struct.unpack("<I", digest[:4])[0]
