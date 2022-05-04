#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import lorem
from src.cipherman import cipher


@pytest.fixture
def file_content():
    content = lorem.paragraph()
    return content


def test_padding(file_content):
    text_padded = cipher.pad(file_content)
    assert len(text_padded) % cipher.BLOCK_SIZE == 0


def test_encrypt(file_content):
    encrypted_text, key = cipher.encrypt(file_content)
    assert file_content != encrypted_text
    assert isinstance(encrypted_text, bytes)
    assert isinstance(key, bytes)


def test_decrypt(file_content):
    cypher_text, key = cipher.encrypt(file_content)
    content_decrypt = cipher.decrypt(cypher_text, key)
    assert file_content == content_decrypt
