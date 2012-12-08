#!/bin/bash

alphabet='abcdefghijklmnopqrstuvwxyz'

for first_letter in $(ls /afs/athena.mit.edu/user)
do
    if [[ "$alphabet" == *"$first_letter"* ]]
    then
	for second_letter in $(ls /afs/athena.mit.edu/user/$first_letter)
	do
	    if [[ "$alphabet" == *"$second_letter"* ]]
	    then
		for athena_name in $(ls /afs/athena.mit.edu/user/$first_letter/$second_letter)
		do
		    echo $athena_name
		done
	    fi
	done
    fi
done

for fucker in $(ls /afs/athena.mit.edu/user/other)
do
    echo $fucker
done