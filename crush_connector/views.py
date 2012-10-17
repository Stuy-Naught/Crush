from django.template import Context, loader
from crush_connector.models import Person, Crush
from django.http import HttpResponse

def register(request):
    t = loader.get_template('crush_connector/index.html')
    c = Context({})
    return HttpResponse(t.render(c))

