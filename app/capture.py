#!/usr/bin/env python3
#capture.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Parses a pflog file and write it into a database.'''

__author__ = 'José Lopes de Oliveira Jr.'


from datetime import datetime

import pyshark
import geoip2.database
from geoip2.errors import AddressNotFoundError

from app.models import db, Capture


class PFLogger:
    '''
    Opens and parses pflog files adding geographical information.

    Args:
        f (string): pflog file name --default: app/data/pflog
        g (string): GeoLite database path --default: app/data/geolite.mmdb

    Writes all data into a database defined in app.models.db.

    '''

    def __init__(self, f, g):
        self.capture = pyshark.FileCapture(f)
        self.geo = geoip2.database.Reader(g)
        Capture.query.delete()  # we want no previous records

    def parser(self):
        counter = 0
        for c in self.capture:
            try:
                cs = [datetime.utcfromtimestamp(float(c.sniff_timestamp)), 
                    c.captured_length, 
                    c['ip'].src, 
                    self.geo.country(c['ip'].src).country.iso_code,
                    c['ip'].dst,
                    self.geo.country(c['ip'].dst).country.iso_code]
            except AddressNotFoundError:
                cs = [c.captured_length, c['ip'].src, None,
                    c['ip'].dst, None]

            try:
                t = c.transport_layer.lower()
                cs += [t, c[t].srcport, c[t].dstport]
            except AttributeError:
                cs += [None, None, None]
            
            db.session.add(Capture(cs[0], cs[1], cs[2], cs[3], 
                cs[4], cs[5], cs[6], cs[7], cs[8]))

            # Less commits, better performance.
            # In fact, it's not quite right, so
            # with 20000 disk usage was diminished 
            # and CPU improved, but there were no 
            # expressive gains above this value.
            counter += 1
            if counter == 20000:
                db.session.commit()
                counter = 0
        db.session.commit()  # last items guaranteed

