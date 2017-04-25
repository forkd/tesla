# Tesla
The main target of this project is to parse a honeypot (OpenBSD) access data to a database.  Then it can be used to retrieve information of possible attacks.

Warning: under development!

Environment preparation:

```
$ git clone https://github.com/forkd/tesla
$ cd tesla
$ virtualenv tesla
$ source tesla/bin/activate
$ pip3 install pyshark geoip2
```


# License
This project is licensed under a MIT license.  See the [msg-extractor](https://github.com/mattgwwalker/msg-extractor) to read its licensing --currently it is GPL.
