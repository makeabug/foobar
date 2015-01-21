#!/bin/bash -x

if [ -z "$FOOBAR_ROOT" ]; then
    export FOOBAR_ROOT=/var/www/foobar/;
fi

if [ -z "$FOOBAR_LOG_ROOT" ]; then
    export FOOBAR_LOG_ROOT=/mnt/logs/foobar/;
fi

ps auxf|grep "foobar/uwsgi.ini"|grep -v grep|awk {'print $2'}|xargs kill -9


echo "wait for foobar to exit...."


echo "done"
cd ${FOOBAR_ROOT}>/dev/null

