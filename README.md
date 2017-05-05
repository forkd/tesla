# Tesla

Tesla aims to parse a OpenBSD access data (`pflog`) to a database, and create JSON from it.  Then that data can be used by another applications to get statistics and graphs of network usage.

Warning: under development!


## Infrastructure

Tesla was developed to work in this architecture:

```
      +-------+    SSH     +---------+
      | Tesla |----------->| OpenBSD |
      +-------+            +---------+
          ^    \_______________  
          |                    | HTTP
          | JSON/SQL           V
    +-----------+          +^^^^^^^^^+
    | Analytics |          ( GeoLite ) 
    +-----------+          +vvvvvvvvv+
```


## Environment Preparation

All the steps described here were based on Fedora 25.  If you aren't running this system, things could be a bit different.  Start with:

```
$ git clone https://github.com/forkd/tesla
$ cd tesla
$ virtualenv tesla
$ source tesla/bin/activate
$ pip3 install -r requirements.txt --upgrade
```

> **Note:** I made a [pull-request to pyshark](https://github.com/KimiNewt/pyshark/pull/198/commits/370d850c6be6cf553677770f9281184b60c8976f) because it uses Exception instead of FileNotFoundError in its `file_capture.py`.  Until they fix it, you should apply it manually.

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

Change `DBPASS` in `app/config.py` according to the password previously defined.   You **really** should change `SECRET_KEY` variable there too.  At this point you should setup those `BSD_*` variables in `app/config.py`, because they'll be necessary to get pflog file ahead.

Edit `/var/lib/pgsql/data/pg_hba.conf` to use md5 from local IPv4 connections.  Remember to reload Postgre's service.

Now, prepare the database:

```
$ sudo -u postgresql psql
> CREATE DATABASE tesla;
> \q
$ python manage.py initdb
```

### First Database Import

Set up the pflog retrieval routine.  In my case, they are located in a server accessed by SSH.  So, I created a passwordless SSH key pair, put the public part on the server and kept the private part in the application machine.

```
$ ssh-keygen -t ed25519 -C 'my@email.com'  # use no password
$ scp generated_key_id_25519.pub user@server:path
$ ssh user@server
> cat generated_key_id_25519 >> /home/newuser/.ssh/authorized_keys
> rm generated_key_id_25519 && exit
$ scp -i generated_key_id_25519 /var/log/pf/pflog .  # test: must download this file without asking for password
```

With access to the OpenBSD machine (and internet access), everything's OK to get raw data, process that, and import into database.  Commands below should do it with no errors (note that the last one can take several minutes to finish).

```
$ python manage.py upd8geo
$ python manage.py upd8db
```


### Testing

You should now be able to run Tesla:

```
$ python manage.py runserver
```

If everything went right, accessing `http://localhost:5000/capture/DATE` (where `DATE` is in format `AAAAMMDD`) or `latest` will get the most recent import in JSON format.

```
$ curl http://localhost:5000/capture/latest
```


# Production

When Tesla is in production, it can be periodically executed by cron (for example), to import pflog files and parse them.  You can also periodically update GeoLite database, but remember it can turn geographical data inconsistent, since an IP address can change between GeoLite versions (theoretically).

As the main idea here is to parse a pflog file, and provide that information in a JSON format, there are no queries to retrieve relevant information from that data.  It should be done in another level, where an analytics tool will process the JSON and answer questions such as the most frequent country or the variation between days.


# Database

The resulting database size depends on the number of data transmitted and received by OpenBSD machine, of course.  Empirically, I noticed that a 145 MB pflog file added ~ 795 K rows in database.

If a local IPv4 address was logged, then GeoLite won't be able to figure out its country, so it'll be recorded as `None`.  The same happens with IP addresses not tracked by GeoLite.  Packets with no transport layer data, will also record as `None` those fields.

Tesla was not tested with IPv6.


# About

Tesla was written by José Lopes to be used at [Cemig](http://cemig.com.br). 

The project that resulted in that OpenBSD machine was named Tesla, in honor of Nikola Tesla (1856-1943).  When I started up this repository, I decided to use that name.


# License

This project is licensed under a MIT license; read `LICENSE` file for more information.

