#!/usr/bin/env python3
#analytics.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Calculates summary from pflog data.'''

__author__ = 'José Lopes de Oliveira Jr.'


from datetime import datetime

from app.models import db, Capture, Summary


def summary():
    date = db.session.query(db.func.min(Capture.date)).scalar()
    count = Capture.query.count()
    size = db.session.query(db.func.sum(Capture.length)).scalar()
    tcp = db.session.query(db.func.count(Capture.length)).filter_by(transport_proto='tcp').scalar()
    udp = db.session.query(db.func.count(Capture.length)).filter_by(transport_proto='udp').scalar()

    db.session.add(Summary(datetime(date.year, date.month, date.day), 
        count, size, tcp, udp))
    db.session.commit()

