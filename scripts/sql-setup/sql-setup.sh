#!/bin/bash
wget http://www.sqlite.org/sqlite-autoconf-3070603.tar.gz &&
tar xvfz sqlite-autoconf-3070603.tar.gz &&
cd sqlite-autoconf-3070603 &&
./configure &&
sed -e '/DEFS =/s/.*/& -DSQLITE_MAX_COLUMN=32767/' Makefile &&
make &&
make install &&


