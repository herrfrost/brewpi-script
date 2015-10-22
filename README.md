


Go 1.5
======

```
bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
source /home/pi/.gvm/scripts/gvm
sudo apt-get install bison
gvm install go1.4
gvm use go1.4
export GOROOT_BOOTSTRAP=$GOROOT
gvm install go1.5
gvm use go1.5 --default
```

InfluxDB 0.9.4.2
================

https://github.com/influxdb/influxdb/blob/master/CONTRIBUTING.md

Source
------

```
mkdir $HOME/gocodez
export GOPATH=$HOME/gocodez
go get github.com/influxdb/influxdb
```

Build
-----

```
cd $GOPATH/src/github.com/influxdb
go get -u -f -t ./...
go build ./...
go install ./...
```

Install
-------

[based on https://www.kuerbis.org/2015/03/influxdb-0-9-auf-dem-raspberry-pi-installieren/]

```
cd $HOME
wget https://raw.githubusercontent.com/influxdb/influxdb/master/scripts/init.sh
sudo mkdir /opt/influxdb
sudo mkdir /opt/influxdb/versions
sudo mkdir /opt/influxdb/versions/0.9.4.2
sudo mkdir /opt/influxdb/versions/0.9.4.2/scripts
cd /opt
sudo cp $HOME/init.sh /opt/influxdb/versions/0.9.4.2/scripts
sudo chmod +x /opt/influxdb/versions/0.9.4.2/scripts/init.sh 
sudo mkdir -p /etc/opt/influxdb

sudo cp $GOPATH/bin/* /opt/influxdb/versions/0.9.4.2/


sudo groupadd influxdb
sudo useradd -M -s /bin/bash -g influxdb -d /home/influxdb influxdb 
sudo chown -R influxdb:influxdb /opt/influxdb/

sudo ln -s /opt/influxdb/versions/0.9.4.2/influx /opt/influxdb/influx
sudo ln -s /opt/influxdb/versions/0.9.4.2/influxd /opt/influxdb/influxd
sudo ln -s /opt/influxdb/versions/0.9.4.2/urlgen /opt/influxdb/urlgen
sudo ln -s /opt/influxdb/versions/0.9.4.2/scripts/init.sh /opt/influxdb/init.sh

cd $HOME
/opt/influxdb/influxd config > $HOME/influxdb.conf
```

(see https://github.com/influxdb/influxdb.com/issues/74)

```
sudo cp /home/pi/influxdb.conf /etc/opt/influxdb/
sudo ln -s /opt/influxdb/init.sh /etc/init.d/influxdb
```

Config
------


modify /etc/opt/influxdb/influxdb.conf

```
[data]
 dir = "/var/lib/influxdb/development/db"
 wal-dir = "/var/lib/influxdb/development/wal"

[meta]
 dir = "/var/lib/influxdb/development/meta"

[hinted-handoff]
 dir = "/var/lib/influxdb/development/hh"

sudo mkdir /var/lib/influxdb
sudo chown influxdb:influxdb /var/lib/influxdb
sudo mkdir /var/log/influxdb
sudo chown influxdb:influxdb /var/log/influxdb

sudo update-rc.d influxdb defaults
```
