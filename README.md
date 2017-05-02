# Tesla

The main target of this project is to parse a OpenBSD access data (`pflog`) to a database and JSON.  Then it can be used to get statistics of network usage.

Warning: under development!

## Environment Preparation

All the steps described here were based on Fedora 25.  If you aren't running this system, somethings could be different.  Start with:

```
$ git clone https://github.com/forkd/tesla
$ cd tesla
$ virtualenv tesla
$ source tesla/bin/activate
$ pip3 install pyshark geoip2 psycopg2 sqlalchemy flask flask-script flask-sqlalchemy
$ cd tesla/app && bash geoip_upd8.sh && cd -
$ export TESLA_
```

Then go to PostgreSQL configuration:

```
# dnf install postgresql-server postgresql-contrib
# systemctl enable postgresql
# postgresql-setup --initdb --unit postgresql
# systemctl start postgresql
$ sudo -u postgres psql
> \password
```

Edit `/var/lib/pgsql/data/pg_hba.conf` to use md5 from local IPv4 connections.  Remember to reload Postgre's service.


Now, let's prepare the database:

```
$ sudo -u postgresql psql
> CREATE DATABASE tesla;
> \q
$ python manage.py initdb
```

Set up the pflog retrieval routine.  In my case, they are located in a server accessed by SSH.  So, I created a passwordless SSH key pair, put the public part on the server and the kept the private part in the application machine.

```
$ ssh-keygen -t ed25519 -C 'my@email.com'  # use no password
$ scp generated_key_id_25519.pub user@server:path
$ ssh user@server
> cat generated_key_id_25519 >> /home/newuser/.ssh/authorized_keys
> rm generated_key_id_25519 && exit
$ scp -i generated_key_id_25519 /var/log/pf/pflog .  # test: must download this file without asking for password
```

Default path for pflog and GeoLite files is `tesla/app/data`.  Setup function `pflog()` in `getdata.py` with your server's  data and run that script:

```
$ python getdata.py geolite
$ python getdata.py pflog
```

Import those files to Tesla's database:

```
$ python manage.py upd8db
```

You should now be able to run Tesla:

```
$ python manage.py runserver
```

If everything is right, open a web browser, and access `localhost:5000/packets`.  The data you just import to database will be shown in JSON format.


# License
This project is licensed under a MIT license.

