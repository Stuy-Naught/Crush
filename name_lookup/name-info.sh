#!/bin/sh

for name in $(cat name_list.txt)
do
    echo $name
    ldapsearch -LLL -x -h ldap-too -b "ou=users,ou=moira,dc=mit,dc=edu" "uid=$name" > user_info/$name
done

#cat name_list.txt
