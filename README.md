# Tesla

Tesla is a tool to parse PFSense's logs in OpenBSD systems (a.k.a. pflog files).  After all data is retrieved, it'll be written in a database and can be delivered in JSON format.


# Installation

Tesla was written to be used in a Docker environment.  The steps here describe how to setup this kind of environment.  The recommended architecture to Tesla is this:

```
                            +-------------+
                            | (I) GeoLite |
                            +-------------+
                                   ^
                                 H |
                                 T |
                                 T |
                                 P |
                                   |
   +------------+   HTTP     +-----------+   postgres    +----------------+
   | (P) Client |----------->| (C) Tesla |-------------->| (C) PostgreSQL |
   +------------+            +-----------+               +----------------+
                                   |
                                 S |
                                 S |
                                 H |
                                   |
                                   V
                            +-------------+
                            | (P) OpenBSD |
                            +-------------+
where:
    * (C): container host
    * (P): physical host
    * (I): internet accessible host
```

## PostgreSQL Host

To create the Postgres container, simply build the image with the Dockerfile provided and run a container --before, edit that file to configure DB user and password:

```
$ cd tesla/app/data/Docker
$ docker build -f Dockerfile.postgres -t img-tesla-pg .
$ docker run --name tesla-pg img-tesla-pg
```

When prompt stops showing messages, type control-c to return to Bash.  Now start the image and take note of its IP address --it'll be needed on Tesla's configuration step:

```
$ docker start tesla-pg
$ docker exec -it tesla-pg ip addr show |grep 172.17
```

At this point PostgreSQL should be up and running, accessible by the username and password defined in `Dockerfile.postgres` and with the IP addr you just saw.  Also, remember that this container will be accessed by Tesla's container via port 5432 by default.

## OpenBSD Host

This host must be accessible by Tesla machine via SSH.  It is extremely important that this connection be made without user intervention.  The preferred way is to setup an OpenSSH server here, generate a SSH key pair, and register the public key in `/home/TESLA-USER/.ssh/authorized_keys`, where `TESLA-USER` must be changed according to your setup.

The common steps to achieve this are (inside Tesla's host --next session):

```
$ ssh-keygen -t ed25519 -C 'my@email.com'  # use no password
$ scp generated_key_id_25519.pub TESLA-USER@openbsd-addr:path
$ ssh TESLA-USER@openbsd-addr
> cat generated_key_id_25519 >> /home/TESLA-USER/.ssh/authorized_keys
> rm generated_key_id_25519 && exit
```

In this project, we assume the pflog files are stored in `/var/log/pf/pflog.0`.  This `pflog.0` is a symlink to the real file, which is rotated every day at 0 AM GMT+0.

## Tesla Host

This is the main machine, that will host Tesla's code.  To build up this container, use the proper Dockerfile and the `requirements.txt`:

```
$ cd tesla/app/data/docker
$ cp ../../../requirements.txt .
$ docker build -f Dockerfile.python -t img-tesla-py .
$ docker run -it --name tesla-py img-tesla-py bash
```

After the last command you'll be on container's shell.  Use vi to edit Tesla's configuration file according to Postgres setup and with the private key to access OpenBSD machine via SSH.  Also, you may want to add some IP addresses in `exclude_ips` list in `tesla/app/queries.py` (`topcc()`) that'll be ignored by that SQL query.

### `tesla/app/config.py`

* `DBUSER`
* `DBPASS`
* `SECRET_KEY`
* `BSD_*`

### `tesla/app/getdata.py`

* `topcc()` > `exclude_ips`

This container must have access to GeoLite URI (`tesla/app/getdata.py`) via port 80, to OpenBSD usually via port 22, and must be accessible by client's machine through port 80, 5000 or whatever port you like.

Pay special attention to `BSD_CERT_PATH`, which should have its permissions set to 0600, because this is the private key used to access automatically OpenBSD machine (read OpenBSD Host section to learn more about it).  You may want to run the sequence of commands described in OpenBSD section here to generate and register the access keys.


# Running

With all the machines and systems setup, Tesla is ready to be run.  First things first, so initialize the database, and download latest GeoLite database:

```
$ python manage.py initdb
$ python manage.py upd8geo
```

All commands **must** be executed without further problems.  With that, you're ready to download and import the pflog file into the database:

```
$ python manage.py upd8db
```

If everything's okay, this command will take about 20 minutes to be executed, so open a beer and wait.  Ein prosit!  Of course you can see the process running some queries in the database (with pgadmin3, for example).

After the importing process, you're able to get those data in JSON format.  Flask is only accessible in localhost via port 5000, but it doesn't fit production environments.  To change that behaviour, run Tesla like this:

```
$ python manage.py runserver -h 0.0.0.0 -p 80
```

It'll force Flask to respond to all connections to that host via port 80.  So take note of that IP address and try to access in the client:

```
http://XXX.XXX.XXX.XXX
```

Tesla's index page must be shown, and you'll ready to use the API.  In a more robust infrastructure, a web server could be setup as a reverse proxy, in order to receive the HTTP requests from clients and pass them to Flask.

## Logs

Use `app/data/tesla.log` for troubleshooting.  This file stores all log messages from Tesla.


# JSON

The JSON interface is available by HTTP.  The URIs Tesla provide are described below:

* `/capture`: returns the latest capture in database --1 day period.
* `/capture/AAAAMMYY`: returns the capture in date YYYYMMDD.
* `/summary`: queries and returns the latest summary --1 day period.
* `/summary/AAAAMMYY`: queries and returns the summary in date YYYYMMDD.
* `/topcc`: queries and returns the top country codes inbound --1 day period.
* `/topcc/YYYYMMDD`: queries and returns the top country codes inbound --1 day period.

## capture

This is the JSON format for capture.  Note that `"capture"` is a list, so it can return many results --and it usually does.

```json
{
  "capture": [
    {
      "date": "Wed, 17 May 2017 00:00:00 GMT",
      "icmp_code": null,
      "icmp_type": null,
      "ip_dst": "XXX.XXX.XXX.XXX",
      "ip_dst_geo": "BR",
      "ip_src": "XXX.XXX.XXX.XXX",
      "ip_src_geo": "CN",
      "ip_ttl": 49,
      "ip_version": 4,
      "length": 140,
      "tcp_dport": 22,
      "tcp_flags": 4,
      "tcp_sport": 10310,
      "udp_dport": null,
      "udp_sport": null
    }
  ],
  "status": "OK"
}
```

## summary

The main structure of summary is described below.  It is important to consider that `count` defines how many packets were exchanged, `size` is the sum of all packets' lengths, and the other fields are self-explanatory.

```json
{
  "status:": "OK",
  "summary": [
    {
      "count": 496079,
      "date": "Wed, 10 May 2017 23:59:59 GMT",
      "icmp": 1537,
      "size": 84956760,
      "tcp": 483798,
      "udp": 10744
    }
  ]
}
```

## topcc

This metric sums all access and group them by country code, so the fields in the result are variable.

```json
{
  "status": "OK",
  "topcc": [
    {
      "BR": 3631,
      "CN": 51817,
      "DE": 103184,
      "FR": 4520,
      "GB": 8069,
      "MX": 4116,
      "NL": 4849,
      "PS": 3050,
      "RU": 3035,
      "SE": 3204,
      "TR": 3160,
      "UA": 3124,
      "US": 12941,
      "date": "Wed, 10 May 2017 23:59:59 GMT"
    }
  ]
}

```

## 404

```json
{
  "status": "not found"
}
```


# Database

Database schema is defined in `app/models.py`, that is self explanatory.

The resulting database (`tesla`) size depends on the number of data transmitted and received by OpenBSD machine, of course.  Empirically, I noticed that a 145 MB pflog file added ~ 795 K rows in the database.

If a local IPv4 address was logged, then GeoLite won't be able to figure out its country, so it'll be recorded as `None`.  The same happens with IP addresses not tracked by GeoLite.  Packets with no transport layer data, will also record as `None` those fields.


# About

Tesla was written by [José Lopes](https://twitter.com/forkd_) to be used at [Cemig](http://cemig.com.br).  It is a **CSIRT Cemig** initiative.

![CSIRT Cemig](app/data/csirt-cemig-logo.png?raw=true "CSIRT Cemig")

The project that resulted in that OpenBSD machine was named 'Tesla' in honor of Nikola Tesla (1856-1943).  When I started up this repository, I decided to use that name.

Thanks to [Vimerson Pereira](https://github.com/viperblack) for the Docker tips.


# License

This project is licensed under a MIT license; read `LICENSE` file for more information.
