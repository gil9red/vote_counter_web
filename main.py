#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import os.path

from flask import Flask, render_template, request, jsonify, send_from_directory

from config import DIR, PORT, VOTE_NAMES, ALLOWED_IP_LIST
from utils import get_ip, get_hostname
from db import Vote, VoteName


app = Flask(__name__)

# TODO:
# logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    name_by_counter: dict[str, int] = {
        name: len(VoteName.add(name).get_actual_votes())
        for name in VOTE_NAMES
    }

    return render_template(
        "index.html",
        title=DIR.name,
        name_by_counter=name_by_counter,
        all_votes=Vote.select(),
        sender_id=get_ip(request),
        allowed_ip_list=ALLOWED_IP_LIST,
    )


@app.route("/add-vote", methods=["POST"])
def add_vote():
    data = request.get_json()
    print(data)

    sender_ip = get_ip(request)

    Vote.add(
        name=data["name"],
        sender_ip=sender_ip,
        sender_hostname=get_hostname(sender_ip),
    )

    return jsonify({"ok": True})


@app.route("/cancel-vote", methods=["POST"])
def cancel_vote():
    data = request.get_json()
    print(data)

    vote = Vote.get_by_id(data["id"])
    vote.cancel(sender_ip=get_ip(request))

    return jsonify({"ok": True})


if __name__ == "__main__":
    # Localhost
    app.debug = True

    # Public IP
    app.run(host='0.0.0.0', port=PORT)
