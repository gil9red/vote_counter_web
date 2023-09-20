#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_from_directory

from config import (
    DIR,
    PORT,
    VOTE_NAMES,
    ALLOWED_IP_LIST,
    IP_BY_SENDER_HOSTNAME,
    ONLY_ALLOWED_IP_LIST_MAY_VOTE,
)
from utils import get_ip, get_hostname
from db import Vote, VoteName


app = Flask(__name__)
app.json.sort_keys = False


def get_datetime_dict(dt: datetime | None) -> dict[str, str | int] | None:
    if not dt:
        return

    return {
        "display": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(dt.timestamp()),
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=DIR.name,
    )


@app.route("/api/add-vote", methods=["POST"])
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


@app.route("/api/cancel-vote", methods=["POST"])
def cancel_vote():
    data = request.get_json()
    print(data)

    vote = Vote.get_by_id(data["id"])
    vote.cancel(sender_ip=get_ip(request))

    return jsonify({"ok": True})


@app.route("/api/counter")
def api_counter():
    sender_ip = get_ip(request)

    return jsonify(
        [
            {
                "name": name,
                "counter": len(VoteName.add(name).get_actual_votes()),
                "append_disabled": (
                    # Включено ограничение на добавление
                    # и IP отправителя отсутствует в разрешенном списке
                    ONLY_ALLOWED_IP_LIST_MAY_VOTE
                    and sender_ip not in ALLOWED_IP_LIST
                ),
            }
            for name in VOTE_NAMES
        ]
    )


@app.route("/api/all")
def api_all():
    sender_ip = get_ip(request)

    return jsonify(
        [
            {
                "id": vote.id,
                "name": vote.name.name,
                "sender_ip": vote.sender_ip,
                "sender_hostname": IP_BY_SENDER_HOSTNAME.get(
                    vote.sender_ip, vote.sender_hostname
                ),
                "append_date": get_datetime_dict(vote.append_date),
                "cancel_date": get_datetime_dict(vote.cancel_date),
                "deletion_disabled": (
                    # Если уже отменено
                    vote.cancel_date is not None
                    or (
                        # IP отправителя не совпадает с тем, кто поставил
                        # и IP отправителя отсутствует в разрешенном списке
                        sender_ip != vote.sender_ip
                        and sender_ip not in ALLOWED_IP_LIST
                    )
                ),
            }
            for vote in Vote.select()
        ]
    )


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static/img"),
        "emoji__do_not_litter.png",
    )


if __name__ == "__main__":
    # Localhost
    app.debug = True

    # Public IP
    app.run(host="0.0.0.0", port=PORT)
