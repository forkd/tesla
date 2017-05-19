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

## Tesla Host

Guarantee that this machine has access to OpenBSD machine via SSH and to GeoLite servers as well (this URI can be seen at `app/getdata.py`).  Grant access to PostgreSQL machine too, via postgres port (commonly 5432).  Since Tesla machine will be the central hub, it has to be accessible by the client which will retrieve data and process it.

>>> Installation steps enter here, like cloning the repo, installing system dependencies etc.

Inside Tesla's directory, setup `app/config.py` with your environment's data, specially:

* `DBUSER`
* `DBPASS`
* `SECRET_KEY`
* `BSD_*`

Pay special attention to `BSD_CERT_PATH`, which should have its permissions set to 0600, because this is the private key used to access automatically OpenBSD machine (read OpenBSD Host section to learn more about it).

## OpenBSD Host

This host must be accessible by Tesla machine via SSH.  It is extremely important that this connection be made without user intervention.  The preferred way is to setup an OpenSSH server here, generate a SSH key pair, and register the public key in `/home/TESLA-USER/.ssh/authorized_keys`, where `TESLA-USER` must be changed according to your reality.

The common steps to achieve this are:

```
$ ssh-keygen -t ed25519 -C 'my@email.com'  # use no password
$ scp generated_key_id_25519.pub user@server:path
$ ssh user@server
> cat generated_key_id_25519 >> /home/TESLA-USER/.ssh/authorized_keys
> rm generated_key_id_25519 && exit
```

In this project, we assume the pflog files are stored in `/var/log/pf/pflog`.  This `pflog` is a symlink to the real file, which is rotated every day at 0 AM GMT+0.

## PostgreSQL Host

Having PostgreSQL up and running, just ensure that it is accessible by Tesla host via that port configured in `app/config.py` --and credentials too.  After that, create the database to store the packets data, usually with `psql` command:

```sql
> create database tesla;
> \q
```

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
* `/topccsrc`: queries and returns the top country codes inbound --1 day period.
* `/topccsrc/YYYYMMDD`: queries and returns the top country codes inbound --1 day period.

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
  "summaries": [
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

## topccsrc

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


# License

This project is licensed under a MIT license; read `LICENSE` file for more information.


#########################################################################

## Environment Preparation

All the steps described here were based on Fedora 25.  If you aren't running this system, things could be a bit different.  Start with:

```
$ git clone https://github.com/forkd/tesla
$ cd tesla
$ virtualenv tesla
$ source tesla/bin/activate
$ pip3 install -r requirements.txt --upgrade
# dnf install wireshark  # for tshark utility
```

From this moment, it'll be considered that all commands will be executed inside this virtual environment. 

### Database Setup

Then go to PostgreSQL installation and configuration:

```
# dnf install postgresql-server postgresql-contrib
# systemctl enable postgresql
# postgresql-setup --initdb --unit postgresql
# systemctl start postgresql
$ sudo -u postgres psql
> \password
> \q
```

Edit `/var/lib/pgsql/data/pg_hba.conf` to use md5 from local IPv4 connections.  Remember to reload Postgre's service.


# Production

When Tesla is in production, it can be periodically executed by cron (for example), to import pflog files and parse them.  You can also periodically update GeoLite database, but remember it can turn geographical data inconsistent, since an IP address can change between GeoLite versions (theoretically).

As the main idea here is to parse a pflog file, and provide that information in a JSON format, there are no queries to retrieve relevant information from that data.  It should be done in another level, where an analytics tool will process the JSON and answer questions such as the most frequent country or the variation between days.

Logging data are recorded by default in `app/data/tesla.log`.

You must set the IP address to `0.0.0.0` in production environments.  As this project uses flask_scripts, this can be done using parameters to `runserver`:

```
$ python manage.py runserver -h 0.0.0.0 -p 80
```

