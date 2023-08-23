#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import unittest
from datetime import datetime

from peewee import SqliteDatabase

from db import (
    BaseModel,
    VoteName,
    Vote,
    db,
)


class TestCaseDB(unittest.TestCase):
    def setUp(self):
        self.models = BaseModel.get_inherited_models()
        self.test_db = SqliteDatabase(":memory:")
        self.test_db.bind(self.models, bind_refs=False, bind_backrefs=False)
        self.test_db.connect()
        self.test_db.create_tables(self.models)

    def test_votes(self):
        vote1 = Vote.add("Foo", "127.0.0.1")
        vote2 = Vote.add("Foo", "127.0.0.1")

        votes = VoteName.get_by("Foo").get_actual_votes()
        self.assertTrue(
            [vote1, vote2], votes
        )

        with self.assertRaises(Exception):
            vote1.cancel(sender_ip="0.0.0.0")

        self.assertIsNone(vote1.cancel_date)
        vote1.cancel(sender_ip=vote1.sender_ip)
        self.assertIsNotNone(vote1.cancel_date)

        votes = VoteName.get_by("Foo").get_actual_votes()
        self.assertTrue(
            [vote1], votes
        )


if __name__ == "__main__":
    unittest.main()
