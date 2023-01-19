#!/usr/bin/env bash

BASEDIR=$(dirname "$0")/$1

mkdir $BASEDIR/
touch $BASEDIR/main.cpp
touch $BASEDIR/input.txt
code $BASEDIR/main.py
cd $BASEDIR/