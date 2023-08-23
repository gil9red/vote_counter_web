#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from subprocess import check_output, STDOUT

from flask import Request


def get_ip(rq: Request) -> str:
    # Proxy
    if rq.environ.get('HTTP_X_FORWARDED_FOR'):
        return rq.environ['HTTP_X_FORWARDED_FOR']

    return rq.environ['REMOTE_ADDR']


def get_hostname(ip: str) -> str | None:
    result: bytes = check_output(["nslookup", "-q=PTR", ip], stderr=STDOUT)

    m = re.search(rb"(\S+)\.employees\.", result)
    if not m:
        return

    return m.group(1).decode("utf-8")


if __name__ == '__main__':
    print(get_hostname("127.0.0.1"))
    # None

    print(get_hostname("10.7.8.31"))
    # ipetrash
