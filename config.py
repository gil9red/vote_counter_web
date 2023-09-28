#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import os

from pathlib import Path


DIR = Path(__file__).resolve().parent

DB_DIR_NAME = DIR / "database"
if path := os.environ.get("DB_DIRECTORY_PATH"):
    DB_DIR_NAME = Path(path).resolve()
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

DB_FILE_NAME = DB_DIR_NAME / "db.sqlite"

PORT = int(os.environ.get("FLASK_RUN_PORT", 10000))

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
IP_BY_SENDER_HOSTNAME: dict[str, str] = json.loads(
    IP_BY_SENDER_HOSTNAME_FILE_NAME.read_text("utf-8")
)

ALLOWED_IP_LIST_FILE_NAME = DIR / "ALLOWED_IP_LIST.json"
if value := os.environ.get("ALLOWED_IP_LIST"):
    ALLOWED_IP_LIST: list[str] = value.split(",")
else:
    ALLOWED_IP_LIST: list[str] = json.loads(
        ALLOWED_IP_LIST_FILE_NAME.read_text("utf-8")
    )

ONLY_ALLOWED_IP_LIST_MAY_VOTE = False
if value := os.environ.get("ONLY_ALLOWED_IP_LIST_MAY_VOTE"):
    ONLY_ALLOWED_IP_LIST_MAY_VOTE = value.lower() == "true"
