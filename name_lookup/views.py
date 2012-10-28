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
    root = ET.fromstring(response_string)
    node = root.find('pre')
    text = node.text
    #crush_info = re.match('<pre>\(.*\)</pre>', response_string).group()
    return HttpResponse(text)
