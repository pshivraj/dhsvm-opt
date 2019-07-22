#!/bin/bash
wget https://www.sqlite.org/src/tarball/sqlite.tar.gz &&
sudo apt-get update
sudo apt-get install build-essential -y
tar xzf sqlite.tar.gz &&
cd sqlite/ &&
./configure &&
make sqlite3.c &&
sed -i 's/\(# define SQLITE_MAX_COLUMN \)\(.*\)/\132000/' sqlite3.c
git clone https://github.com/coleifer/pysqlite3 &&
cd pysqlite3 &&
cp ../sqlite3.[ch] . &&
python setup.py build_static &&
python setup.py install


