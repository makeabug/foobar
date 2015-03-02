#!/bin/bash -x

if [ -z "$FOOBAR_ROOT" ]; then
    export FOOBAR_ROOT=/var/www/foobar/;
fi

if [ -z "$FOOBAR_LOG_ROOT" ]; then
    export FOOBAR_LOG_ROOT=/var/logs/foobar/;
fi

ps auxf|grep "foobar/uwsgi.ini"|grep -v grep|awk {'print $2'}|xargs kill -9


echo "wait for foobar to exit...."

sleep 1

echo "starting foobar...."
cd ${FOOBAR_ROOT} >/dev/null
python manage.py syncdb
python manage.py compilemessages
#python manage.py collectstatic
echo >${FOOBAR_LOG_ROOT}foobar.log

rm -f ${FOOBAR_LOG_ROOT}uwsgi.log
uwsgi --ini foobar/uwsgi.ini --daemonize ${FOOBAR_LOG_ROOT}uwsgi.log

echo "done"
cd ${FOOBAR_ROOT}>/dev/null

