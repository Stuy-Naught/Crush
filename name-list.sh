#!/bin/bash

for first_letter in $(ls /afs/athena.mit.edu/user)
do
    for second_letter in $(ls /afs/athena.mit.edu/user/$first_letter)
    do
	for athena_name in $(ls /afs/athena.mit.edu/user/$first_letter/$second_letter)
	do
	    echo $athena_name
	done
    done
done