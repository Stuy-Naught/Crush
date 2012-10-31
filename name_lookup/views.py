import urllib2
import re
import subprocess
from models import *
from django.http import HttpResponse, HttpResponseRedirect
import json
import time

from crush_connector.models import Person, Crush
from crush_connector.forms import RegisterForm

def mit_info(username):
    fixed_string = re.sub(' ', '+', username)
    fixed_string = re.sub('@mit.edu', '', fixed_string)
    response = urllib2.urlopen('http://web.mit.edu/bin/cgicso?options=general&query=%s' % fixed_string)
    response_string = ' '.join([s[:-1] for s in response.readlines()])
    info = re.match('.*<PRE>(.*)</PRE>', response_string).group(1)
    m = re.match('\s*name:(.*)\s*email: <A.*>(.*)</A>\s*address: (.*)\s*year: (.*)', info)

    if m is not None:
        name = m.group(1).strip()
        email = m.group(2).strip()
        address = m.group(3).strip()
        year = m.group(4).strip()
    
        return {"name": name, "email": email, "address": address, "year": year}

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
        person.name = info['year']
    person.save()

def ls(dir):
    return subprocess.check_output('ls %s' % dir).split('\n')

def populate_names(request):
    print('starting populate_names')
    names = subprocess.check_output('name_lookup/name-list.sh').split('\n')
    names = names[2000:2020]
    print names
    print('done getting name list')
    print('starting MIT people lookups')
    for username in names:
        print('  finding %s' % username)
        set_user_info(username)
        time.sleep(0.1)
    print('done MIT people lookups')
    
    #base_dir = '/afs/athena.mit.edu/user'
    #for first_letter in ls(base_dir):
    #    for second_letter in ls('%s/%s' % (base_dir, first_letter)):
    #        for athena_name in ls('%s/%s/%s' % (base_dir, first_letter, second_letter)):
    #            set_user_info(athena_name)
                
