#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
from datetime import datetime

import flask
import flask_login

from config import (
    DIR,
    PORT,
    VOTE_NAMES,
    LOGIN,
    PASSWORD,
    SECRET_KEY
)
from db import Vote, VoteName


# Our mock database.
USERS = {
    LOGIN: {
        "password": PASSWORD,
    },
}


app = flask.Flask(__name__)
app.secret_key = SECRET_KEY
app.json.sort_keys = False

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    @classmethod
    def create(cls, login: str) -> "User":
        user = User()
        user.id = login
        return user


# Если авторизован
@login_manager.user_loader
def user_loader(login):
    if login not in USERS:
        return

    return User.create(login)


# Если не авторизован
@login_manager.request_loader
def request_loader(request):
    login = request.form.get("login")
    if login not in USERS:
        return

    return User.create(login)


def get_datetime_dict(dt: datetime | None) -> dict[str, str | int] | None:
    if not dt:
        return

    return {
        "display": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(dt.timestamp()),
    }


@app.route("/")
def index():
    return flask.render_template(
        "index.html",
        title=DIR.name,
    )


@app.route("/api/add-vote", methods=["POST"])
@flask_login.login_required
def add_vote():
    data = flask.request.get_json()
    print(data)

    sender_login = flask_login.current_user.id

    Vote.add(
        name=data["name"],
        sender_login=sender_login,
    )

    return flask.jsonify({"ok": True})


@app.route("/api/cancel-vote", methods=["POST"])
@flask_login.login_required
def cancel_vote():
    data = flask.request.get_json()
    print(data)

    vote = Vote.get_by_id(data["id"])
    vote.cancel()

    return flask.jsonify({"ok": True})


@app.route("/api/counter")
def api_counter():
    is_authenticated = flask_login.current_user.is_authenticated

    return flask.jsonify(
        [
            {
                "name": name,
                "counter": len(VoteName.add(name).get_actual_votes()),
                "append_disabled": not is_authenticated,
            }
            for name in VOTE_NAMES
        ]
    )


@app.route("/api/all")
def api_all():
    is_authenticated = flask_login.current_user.is_authenticated

    return flask.jsonify(
        [
            {
                "id": vote.id,
                "name": vote.name.name,
                "sender_login": vote.sender_login,
                "append_date": get_datetime_dict(vote.append_date),
                "cancel_date": get_datetime_dict(vote.cancel_date),
                "deletion_disabled": (
                    # Если уже отменено или не авторизован
                    vote.cancel_date is not None or not is_authenticated
                ),
            }
            for vote in Vote.select()
        ]
    )


@app.route("/login", methods=["POST"])
def login():
    login = flask.request.form["login"]
    if login in USERS and flask.request.form["password"] == USERS[login]["password"]:
        remember = "remember_me" in flask.request.form

        user = User.create(login)
        flask_login.login_user(user, remember)
        return flask.jsonify({"ok": True})

    return flask.jsonify({
        "ok": False,
        "error": "Неправильный логин и/или пароль",
    })


@app.route("/logout", methods=["GET"])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/favicon.ico")
def favicon():
    return flask.send_from_directory(
        os.path.join(app.root_path, "static/img"),
        "emoji__do_not_litter.png",
    )


if __name__ == "__main__":
    # Localhost
    app.debug = True

    # Public IP
    app.run(host="0.0.0.0", port=PORT)
