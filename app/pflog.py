#!/usr/bin/env python3
# pflog.py
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
        f (string): pflog file name
        g (string): GeoLite database path

    Writes all data into a database defined in app.models.db.

    '''

    def __init__(self, f, g):
        self.capture = pyshark.FileCapture(f)
        self.geo = geoip2.database.Reader(g)

    def parser(self):
        for c in self.capture:
            p = [c.captured_length, c['ip'].src, 
                self.geo.country(c['ip'].src).country.iso_code,
                c['ip'].dst,
                self.geo.country(c['ip'].dst).country.iso_code]

            try:
                p += [c.transport_layer.lower(), 
                    c[c.transport_layer.lower()].srcport, 
                    c[c.transport_layer.lower()].dstport]
            except AttributeError:
                p += [None, None, None]
            
            # write to database
            db.session.add(Packet(p[0], p[1], p[2], p[3], 
                p[4], p[5], p[6], p[7]))
            db.session.commit()


if __name__ == "__main__":
    # TODO: when running as program this script 
    # should parse the pflog file and write it 
    # into the database.
    PFLogger('pflog.0', 'geolite.mmdb').parser()

