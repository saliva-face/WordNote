import hashlib
import os

def pwg(text):
    text = str(text).encode("utf-8")
    salt = str(os.urandom(32)).encode("utf-8")
    result = salt + text
    for i in range(200001):
        result = hashlib.sha256(result).hexdigest().encode("utf-8")
    return result.decode("utf-8"), salt.decode("utf-8")

def pwc(text, salt):
    text = str(text).encode("utf-8")
    salt = str(salt).encode("utf-8")
    result = salt + text
    for i in range(200001):
        result = hashlib.sha256(result).hexdigest().encode("utf-8")
    return result.decode("utf-8")