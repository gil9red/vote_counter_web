#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
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

IP_BY_SENDER_HOSTNAME_FILE_NAME = DIR / "IP_BY_SENDER_HOSTNAME.json"
IP_BY_SENDER_HOSTNAME = json.loads(
    IP_BY_SENDER_HOSTNAME_FILE_NAME.read_text("utf-8")
)

ALLOWED_IP_LIST = [
    "127.0.0.1",
]
