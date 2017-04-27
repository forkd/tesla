#!/bin/bash
#geoip_upd8.sh
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz -O geolite.tgz
tar -xzvf geolite.tgz
mv GeoLite*/*.mmdb ../geolite.mmdb
rm -rf geolite.tgz GeoLite*

