# Tesla

Tesla aims to parse a OpenBSD access data (`pflog`) to a database, and create JSON from it.  Then that data can be used by another applications to get statistics and graphs of network usage.

Warning: under development!

## Environment Preparation

All the steps described here were based on Fedora 25.  If you aren't running this system, things could be a bit different.  Start with:

```
$ git clone https://github.com/forkd/tesla
$ cd tesla
$ virtualenv tesla
$ source tesla/bin/activate
$ pip3 install pyshark geoip2 psycopg2 sqlalchemy flask flask-script flask-sqlalchemy
$ cd tesla/app && bash geoip_upd8.sh && cd -
```

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

Now, prepare the database:

```
$ sudo -u postgresql psql
> CREATE DATABASE tesla;
> \q
$ python manage.py initdb
```

### First Database Import

Set up the pflog retrieval routine.  In my case, they are located in a server accessed by SSH.  So, I created a passwordless SSH key pair, put the public part on the server and the kept the private part in the application machine.

```
$ ssh-keygen -t ed25519 -C 'my@email.com'  # use no password
$ scp generated_key_id_25519.pub user@server:path
$ ssh user@server
> cat generated_key_id_25519 >> /home/newuser/.ssh/authorized_keys
> rm generated_key_id_25519 && exit
$ scp -i generated_key_id_25519 /var/log/pf/pflog .  # test: must download this file without asking for password
```

Default path for pflog and GeoLite files is `tesla/app/data`.  Setup `pflog()` in `getdata.py` with your server's data and download the base files --`geolite()` will require internet access and `pflog()` will require access to your server:

```
$ python manage.py geolite
$ python manage.py pflog
```

Import those files to Tesla's database --it may take some minutes according to your pflog file:

```
$ python manage.py upd8db
```

### Testing

You should now be able to run Tesla:

```
$ python manage.py runserver
```

If everything went right, open a web browser, and access `localhost:5000/packets`.  The data you just imported to database will be shown in JSON format.


# License

This project is licensed under a MIT license.

