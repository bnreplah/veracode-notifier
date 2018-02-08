import os
import time
from hashlib import sha256
import hmac
import codecs


def _get_creds():
    return os.environ.get("VERACODE_API_KEY_ID"), os.environ.get("VERACODE_API_KEY_SECRET")


def _get_timestamp():
    return int(round(time.time() * 1000))


def _get_nonce():
    return os.urandom(16).hex()


def _create_signature(api_secret, signing_data, timestamp, nonce):
    key_nonce = hmac.new(codecs.decode(api_secret, "hex_codec"), codecs.decode(nonce, "hex_codec"), sha256).digest()
    key_date = hmac.new(key_nonce, str(timestamp).encode(), sha256).digest()
    signature_key = hmac.new(key_date, u"vcode_request_version_1".encode(), sha256).digest()
    return hmac.new(signature_key, signing_data.encode(), sha256).hexdigest()


def generate_veracode_hmac_header(host, url, method):
    api_id, api_secret = _get_creds()
    signing_data = "id={api_id}&host={host}&url={url}&method={method}".format(api_id=api_id.lower(),
                                                                              host=host.lower(),
                                                                              url=url, method=method.upper())
    timestamp = _get_timestamp()
    nonce = _get_nonce()
    signature = _create_signature(api_secret, signing_data, timestamp, nonce)
    return "{auth_scheme} id={id},ts={ts},nonce={nonce},sig={sig}".format(auth_scheme="VERACODE-HMAC-SHA-256", id=api_id,
                                                                          ts=timestamp, nonce=nonce, sig=signature)
