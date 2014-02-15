#!/bin/bash
#git doesn't do keyword expansion inside a file. This script generates a version string
#after each commit which would be suitable for an after-commit script that subs the
#version into version-controlled files.
revisioncount=`git log --oneline | wc -l`
projectversion=`git describe --tags --long`
ERR=$?
if [[ ${ERR} -ne 0 ]]; then
    >&2 echo "ERROR getting project version tag."
    exit 2
fi
cleanversion=${projectversion%%-*}

if [[ $# -gt 0 ]]; then
  if [[ $1 == clean ]]; then
	echo "$cleanversion.$revisioncount"
  else
	>&2 echo "Only argument accepted is 'clean'" 
        exit 1
  fi
else
	echo "$projectversion-$revisioncount"
fi
