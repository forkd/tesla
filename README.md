# Tesla
The main target of this project is to parse a honeypot (OpenBSD) access data to a database.  Then it can be used to retrieve information of possible attacks.

Warning: under development!

Environment preparation:

```
$ git clone https://github.com/forkd/tesla
$ cd tesla
$ virtualenv tesla
$ source tesla/bin/activate
$ pip3 install pyshark geoip2 pycopg2 sqlalchemy flask flask-script flask-sqlalchemy
```

For PostgreSQL:

```
# dnf install postgresql-server postgresql-contrib
# systemctl enable postgresql
# postgresql-setup --initdb --unit postgresql
# systemctl start postgresql
$ sudo -u postgres psql
> \password
```

Edit /var/lib/pgsql/data/pg_hba.conf to use md5 from local IPv4 connections.  Remember to reload Postgre's service.


Database

Create and initialize the database:

```
$ sudo -u postgresql psql
> CREATE DATABASE tesla;
> \q
$ python manage.py initdb
```

Assuming pflog and GeoLite files are in the current directory, populate the database:

```
$ python manage.py upd8db
```


# License
This project is licensed under a MIT license.  See the [msg-extractor](https://github.com/mattgwwalker/msg-extractor) to read its licensing --currently it is GPL.
