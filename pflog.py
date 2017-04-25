#!/usr/bin/env python3
# pflog.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''
Parses a pflog file into a database writable format.

'''

__author__ = 'José Lopes de Oliveira Jr.'


import pyshark
import geoip2.database


class PFLogger:
    '''
    Opens and parses pflog files adding geographical information.

    Args:
        f (string): pflog file name
        g (string): GeoLite database path

    '''

    def __init__(self, f, g):
        self.capture = pyshark.FileCapture(f)
        self.geo = geoip2.database.Reader(g)

    def parser(self):
        packets = list()

        for c in self.capture:
            p = [c.captured_length, c['ip'].dst, 
                self.geo.country(c['ip'].dst).country.iso_code,
                c['ip'].src,
                self.geo.country(c['ip'].src).country.iso_code]

            try:
                p += [c.transport_layer.lower(), 
                    c[c.transport_layer.lower()].dstport, 
                    c[c.transport_layer.lower()].srcport]
            
            except AttributeError:
                p += [None, None, None]
            
            packets.append(p)
            print(p)


if __name__ == "__main__":
    PFLogger('pflog.0', 'geolite.mmdb').parser()

