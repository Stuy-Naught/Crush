import urllib2
import re
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from crush_connector.models import Person, Crush
from crush_connector.forms import RegisterForm

def lookup_mit_people(request, string):
    fixed_string = re.sub(' ', '+', string)
    fixed_string = re.sub('@mit.edu', '', fixed_string)
    response = urllib2.urlopen('http://web.mit.edu/bin/cgicso?options=general&query=%s' % fixed_string)
    response_string = ' '.join(response.readlines())
    return HttpResponse(response_string)
