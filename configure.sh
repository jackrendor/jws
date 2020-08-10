#!/usr/bin/env bash
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
virtualenv -p python3 "$SCRIPTPATH"/venv
source "$SCRIPTPATH"/venv/bin/activate
pip3 install -r ./requirements.txt
