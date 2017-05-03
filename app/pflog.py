#!/usr/bin/env python3
#pflog.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''
Parses a pflog file and write it into a database.  This
script can be used as a module or as an independent
program.

'''

__author__ = 'José Lopes de Oliveira Jr.'


import pyshark
import geoip2.database

from app.models import db, Packet


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

    def parser(self):
        counter = 0
        for c in self.capture:
            p = [c.captured_length, c['ip'].src, 
                self.geo.country(c['ip'].src).country.iso_code,
                c['ip'].dst,
                self.geo.country(c['ip'].dst).country.iso_code]

            try:
                t = c.transport_layer.lower()
                p += [t, c[t].srcport, c[t].dstport]
            except AttributeError:
                p += [None, None, None]
            
            db.session.add(Packet(p[0], p[1], p[2], p[3], 
                p[4], p[5], p[6], p[7]))

            # the less we commit, the better we perform
            counter += 1
            if counter == 20000:
                db.session.commit()
                counter = 0
        db.session.commit()  # last items guaranteed


if __name__ == "__main__":
    # TODO: when running as program this script 
    # should parse the pflog file and write it 
    # into the database.
    PFLogger('app/data/pflog', 'app/data/geolite.mmdb').parser()

