#!/bin/sh

if [ "$1" != "" ]; then
    echo "Creating comments table"
    psql -h localhost -d $1 -U admin -w -f comments.sql
    echo "Created"
else
    echo "no database chosen"
fi
