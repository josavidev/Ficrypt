#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path, remove

import pytest
import lorem
from src.cipherman import fileman, cipher

TEST_FILE_PATH = './tests/new.txt'
NEW_LINE_BYTES = '\n'.encode('utf-8')


@pytest.fixture
def autogen_content():
    content = lorem.paragraph()
    yield content
    remove(TEST_FILE_PATH)


def test_write_file(autogen_content):
    fileman.write_bytes_file(autogen_content.encode('utf-8'), TEST_FILE_PATH)
    assert path.exists(TEST_FILE_PATH)


def test_read_bytes_file(autogen_content):
    fileman.write_bytes_file(autogen_content.encode('utf-8'), TEST_FILE_PATH)
    content_file = fileman.read_bytes_file(TEST_FILE_PATH)
    assert content_file == autogen_content.encode('utf-8')


def test_read_file(autogen_content):
    fileman.write_bytes_file(autogen_content.encode('utf-8'), TEST_FILE_PATH)
    content_file = fileman.read_file(TEST_FILE_PATH)
    assert content_file == autogen_content


def test_write_encrypted_bytes(autogen_content):
    encrypted_content, _ = cipher.encrypt(autogen_content)
    fileman.write_bytes_file(encrypted_content, TEST_FILE_PATH)
    content_file = fileman.read_bytes_file(TEST_FILE_PATH)
    assert path.exists(TEST_FILE_PATH)
    assert encrypted_content == content_file
