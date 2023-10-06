#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


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

LOGIN = os.environ.get("ADMIN_LOGIN", "admin")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

SECRET_KEY = os.environ.get("SECRET_KEY", "super secret string")
