import hashlib
import hmac
import base64


def hmac_sha256(data, key):
    message = bytes(data, 'utf-8')
    secret = bytes(key, 'utf-8')
    return base64.b64encode(hmac.new(secret, message, hashlib.sha256).digest())
