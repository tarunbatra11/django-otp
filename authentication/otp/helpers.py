import binascii
import os


def generate_secret_identifier():
    identifier = binascii.hexlify(os.urandom(24))
    return identifier
