#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from datetime import datetime
from typing import Type, Iterable, TypeVar, Optional

# pip install peewee
from peewee import (
    Model,
    TextField,
    ForeignKeyField,
    DateTimeField,
    CharField,
)
from playhouse.shortcuts import model_to_dict
from playhouse.sqliteq import SqliteQueueDatabase

from config import DB_FILE_NAME, ALLOWED_IP_LIST
from third_party.shorten import shorten


# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        "foreign_keys": 1,
        "journal_mode": "wal",  # WAL-mode
        "cache_size": -1024 * 64,  # 64MB page-cache
    },
    use_gevent=False,  # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,  # Max. # of pending writes that can accumulate.
    results_timeout=5.0,  # Max. time to wait for query to be executed.
)


ChildModel = TypeVar("ChildModel", bound="BaseModel")


class BaseModel(Model):
    class Meta:
        database = db

    def get_new(self) -> ChildModel:
        return type(self).get(self._pk_expr())

    @classmethod
    def get_first(cls) -> ChildModel:
        return cls.select().first()

    @classmethod
    def get_last(cls) -> ChildModel:
        return cls.select().order_by(cls.id.desc()).first()

    @classmethod
    def get_inherited_models(cls) -> list[Type["BaseModel"]]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def print_count_of_tables(cls):
        items = []
        for sub_cls in cls.get_inherited_models():
            name = sub_cls.__name__
            count = sub_cls.select().count()
            items.append(f"{name}: {count}")

        print(", ".join(items))

    @classmethod
    def count(cls, filters: Iterable = None) -> int:
        query = cls.select()
        if filters:
            query = query.filter(*filters)
        return query.count()

    def to_dict(self) -> dict:
        return model_to_dict(self)

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if v:
                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f"{k}_id"
                if v:
                    v = v.id

            fields.append(f"{k}={v}")

        return self.__class__.__name__ + "(" + ", ".join(fields) + ")"


class VoteName(BaseModel):
    name = TextField(unique=True)

    @classmethod
    def get_by(cls, name: str) -> Optional["VoteName"]:
        return cls.get_or_none(name=name)

    @classmethod
    def add(cls, name: str) -> "VoteName":
        obj = cls.get_by(name)
        if not obj:
            obj = cls.create(name=name)

        return obj

    def get_actual_votes(self) -> list["Vote"]:
        return list(self.votes.where(Vote.cancel_date.is_null(True)))


class Vote(BaseModel):
    name = ForeignKeyField(VoteName, backref="votes")
    sender_ip = TextField()
    sender_hostname = TextField(null=True)
    append_date = DateTimeField(default=datetime.now)
    cancel_date = DateTimeField(null=True)

    @classmethod
    def add(cls, name: str, sender_ip: str, sender_hostname: str = None) -> "Vote":
        return cls.create(
            name=VoteName.add(name),
            sender_ip=sender_ip,
            sender_hostname=sender_hostname,
        )

    def cancel(self, sender_ip: str):
        if sender_ip != self.sender_ip and sender_ip not in ALLOWED_IP_LIST:
            raise Exception("Отмена голоса запрещена!")

        self.cancel_date = datetime.now()
        self.save()


db.connect()
db.create_tables(BaseModel.get_inherited_models())

# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)


if __name__ == "__main__":
    BaseModel.print_count_of_tables()
