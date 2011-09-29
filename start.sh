#!/bin/sh

export PYTHONPATH=`pwd`/../
if [ "x$1" == "x" ];
    then
    python manager.py
else
    python manager.py --port="$1"
fi