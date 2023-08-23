#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


DIR = Path(__file__).resolve().parent

DB_DIR_NAME = DIR / "database"
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

DB_FILE_NAME = DB_DIR_NAME / "db.sqlite"

PORT = 10000

VOTE_NAMES = [
    "TXI",
    "RX",
    "TXISS",
    "TXACQ",
    "TXFIN",
    "TXDC",
    "TXCORE",
]
ALLOWED_IP_LIST = [
    "127.0.0.1",
]
