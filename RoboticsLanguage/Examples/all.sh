#!/bin/sh

find . -iname \*.rol | sort | xargs -n 1 rol $1 $2 $3 $4 $5 $6 $7 $8 $9
