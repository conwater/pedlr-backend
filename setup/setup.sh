#!/bin/bash
if [ -z $1 ]
then
	echo "Defaulting to current directory for python venv creation"
	VENVDIR="$(pwd)/venv"
elif [ ! -d $(dirname $1) ]
then
	echo "\"$(dirname $1)\" doesn't exist, exiting script"
	exit
else
	VENVDIR=$1
fi

if [ -f $VENVDIR -o -d $VENVDIR ]
then
	echo "\"$VENVDIR\" already exists, exiting script"
	exit
fi
VENVDIR=$(readlink -f $VENVDIR)
python3 -m venv $VENVDIR
echo "Created virtual environment \"$VENVDIR\""
source $VENVDIR/bin/activate
pip install -r requirements.txt
echo "Installed required python packages in \"$VENVDIR\""
echo "Done"
