#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def write_bytes_file(content: bytes, filepath: str) -> None:
    with open(filepath, 'wb') as file:
        file.write(content)


def read_bytes_file(filepath: str) -> bytes:
    lines = ''.encode('utf-8')
    with open(filepath, 'rb') as file:
        lines = file.read()
    return lines


def read_file(filepath: str) -> str:
    lines = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return ''.join(lines)


def write_file(content: bytes, filepath: str) -> None:
    with open(filepath, 'w') as file:
        file.write(content)
