import urllib2
import re
import subprocess
from models import *
from django.http import HttpResponse, HttpResponseRedirect
import json
import time
import os

from crush_connector.models import Person, Crush
from crush_connector.forms import RegisterForm

def mit_info(username):
#    command = 'ldapsearch -LLL -x -h ldap-too -b "ou=users,ou=moira,dc=mit,dc=edu" "uid=%s"' % username
#    print command
#    info = subprocess.check_output(command)
    print('working dir: %s' % os.getcwd())

    info = open('name_lookup/user_info/%s' % username, 'r').readlines()
    print info

    if info is not None:
        fields = ['name', 'email', 'address', 'year']
        regexes = {}
        info_res = {}
        
        
        regexes['name'] = 'displayName: (.*)'
        regexes['email'] = 'mail: (.*)'
        regexes['address'] = 'street: (.*)'
        regexes['year'] = 'mitDirStudentYear: (.*)'
        
        for field in fields:
            for line in info:
                try:
                    matched_text = re.match(regexes[field], line).group(1).strip()
                    info_res[field] = matched_text # do this on two lines so as not to overwrite info_res after it's already been found
                except:
                    pass
            if 'email' not in info_res:
                info_res['email'] = username + '@mit.edu'
            if 'name' not in info_res:
                info_res['name'] = username
                info_res['email'] = username + '@mit.edu'
            if 'year' in info_res:
                try:
                    info_res['year'] = int(info_res['year'])
                except:
                    del info_res['year']
        return info_res
    
    return {"email": "%s@mit.edu" % username}

def lookup_mit_people(request, username):
    info = mit_info(username)
    return HttpResponse(json.dumps(info))

def set_user_info(username):
    person, created = Person.objects.get_or_create(email = username + '@mit.edu')
    person.save()
    info = mit_info(username)
    person.email = info['email']
    if 'name' in info:
        person.name = info['name']
    if 'address' in info:
        person.address = info['address']
    if 'year' in info:
        person.year = info['year']
    person.save()

def ls(dir):
    return subprocess.check_output('ls %s' % dir).split('\n')

def populate_names(request):
    print('starting populate_names')
    print('working dir: %s' % os.getcwd())
    #names = subprocess.check_output('name_lookup/name-list.sh').split('\n')
    names = open('name_lookup/name_list.txt', 'r').readlines()
    names = [name.strip() for name in names]
    #names = names[13460:13470]
    print names
    print('done getting name list')
    print('starting MIT people lookups')
    for username in names:
        print('  finding %s' % username)
        set_user_info(username)
        time.sleep(0.5)
    print('done MIT people lookups')
    
    #base_dir = '/afs/athena.mit.edu/user'
    #for first_letter in ls(base_dir):
    #    for second_letter in ls('%s/%s' % (base_dir, first_letter)):
    #        for athena_name in ls('%s/%s/%s' % (base_dir, first_letter, second_letter)):
    #            set_user_info(athena_name)
                
