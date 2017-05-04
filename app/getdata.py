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
from os import remove, system, path, makedirs
from urllib.request import urlretrieve
from glob import glob
from shutil import move, rmtree

from app.config import Production


if not path.isdir(Production().BASE_DATA_PATH):
    makedirs(Production().BASE_DATA_PATH)


def geolite(dp, gf):
    url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz'
    filepath = '{0}/{1}.tgz'.format(dp, gf)
    urlretrieve(url, filepath)  # tarfile only works with files
    compacted = tarfile.open(filepath, mode='r:gz')
    mmdbfile = None
    regex = re.compile(r'^.+\.mmdb$')

    for f in compacted.getnames():
        if regex.match(f):
            mmdbfile = compacted.getmember(f)
    compacted.extract(mmdbfile, dp, set_attrs=False)
    
    # cleaning up the house
    for f in glob(r'{}/GeoLite2*/GeoLite2*.mmdb'.format(dp)):
        move(f, '{0}/{1}'.format(dp, gf))
    for d in glob(r'{}/GeoLite2*'.format(dp)):
        rmtree(d)
    remove(filepath)

def pflog(dp, pf, c, u, a, r):
    p = Production()
    try:
        remove('{0}/{1}'.format(dp, pf))
    except FileNotFoundError:
        pass
    system('scp -i {0} {1}@{2}:{3} {4}/{5}'.format(c, u, a, r, dp, pf))

