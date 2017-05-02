#!/usr/bin/env python3
#getdata.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''Retrieves GeoLite's mmdb or pflog file.'''

__author__ = 'José Lopes de Oliveira Jr.'


import sys
import re
import tarfile
from os import remove, system
from urllib.request import urlretrieve
from glob import glob
from shutil import move, rmtree


datapath = 'app/data'


def geolite():
    url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz'
    filepath = '{}/geolite.tgz'.format(datapath)
    urlretrieve(url, filepath)  # tarfile only works with files
    compacted = tarfile.open(filepath, mode='r:gz')
    mmdbfile = None
    regex = re.compile(r'^.+\.mmdb$')

    for f in compacted.getnames():
        if regex.match(f):
            mmdbfile = compacted.getmember(f)
    compacted.extract(mmdbfile, datapath)
    
    # cleaning the house
    for f in glob(r'{}/GeoLite2*/GeoLite2*.mmdb'.format(datapath)):
        move(f, '{}/geolite.mmdb'.format(datapath))
    for d in glob(r'{}/GeoLite2*'.format(datapath)):
        rmtree(d)
    remove(filepath)

def pflog():
    cert = 'ssh-private-key-path'
    user = 'username'
    server = 'server-addr'
    remote = 'remote/file/path'
    system('scp -i {0} {1}@{2}:{3} {4}'.format(cert, user, server, 
        remote, datapath))


if __name__ == '__main__':
    try:
        if (sys.argv[1] == 'geolite'):
            geolite()
        elif (sys.argv[1] == 'pflog'):
            pflog()
        else:
            print('Invalid parameter.')
            exit(1)
    except IndexError:
        print('Parameter: geolite or pflog.')

