import urllib2
import re
import xml.etree.ElementTree as ET
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from crush_connector.models import Person, Crush
from crush_connector.forms import RegisterForm

def lookup_mit_people(request, string):
    fixed_string = re.sub(' ', '+', string)
    fixed_string = re.sub('@mit.edu', '', fixed_string)
    response = urllib2.urlopen('http://web.mit.edu/bin/cgicso?options=general&query=%s' % fixed_string)
    response_string = ' '.join([s[:-1] for s in response.readlines()])
    info = re.match('.*<PRE>(.*)</PRE>', response_string).group(1)
    m = re.match('\s*name:(.*)\s*email: <A.*>(.*)</A>\s*address: (.*)\s*year: (.*)', info)

    name = m.group(1).strip()
    email = m.group(2).strip()
    address = m.group(3).strip()
    year = m.group(4).strip()
    
    return HttpResponse('{"name": "%s", "email": "%s", "address": "%s", "year": "%s"}' % (name, email, address, year))
