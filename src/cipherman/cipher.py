#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

from Crypto import Random
from Crypto.Cipher import AES

# set to 16 because the input string should be a multiple of 16 in AES
BLOCK_SIZE = 16
# padding is used to fill up the block by appending some additional bytes.
PAD_CHR = chr(1)


def diffblockmultiple(i: int) -> int:
    return BLOCK_SIZE - i if i <= BLOCK_SIZE else BLOCK_SIZE - i % BLOCK_SIZE


def pad(s: str) -> str:
    return s + PAD_CHR * diffblockmultiple(len(s))


def unpad(s: str) -> str:
    return s[:-s.count(PAD_CHR)] if s[-1] == PAD_CHR else s


def encrypt(plain_text: str):
    key = Random.new().read(AES.block_size)
    private_key = hashlib.sha256(key).digest()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    content_encrypted = cipher.encrypt(pad(plain_text).encode('utf-8'))
    return (iv + content_encrypted), key


def decrypt(cipher_text: bytes, key: bytes) -> str:
    private_key = hashlib.sha256(key).digest()
    iv = cipher_text[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    plain_bytes = cipher.decrypt(cipher_text[16:])
    plain_text = plain_bytes.decode('utf-8')
    return unpad(plain_text)
