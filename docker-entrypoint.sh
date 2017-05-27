#!/bin/sh
python control-server/configure.py
service haproxy start
python control-server/server.py
