from models import *
from django.core.mail import send_mail
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from crush_connector.models import Person, Crush
from crush_connector.forms import RegisterForm

def isMatch(Person1, Person2):
    crushes = Crush.objects.all()
    one_likes_two = False
    two_likes_one = False
    for crush in crushes:
        if (crush.crusher == Person1 and crush.crushee == Person2):
            one_likes_two = True
        if (crush.crusher == Person2 and crush.crushee == Person1):
            two_likes_one = True
    return one_likes_two and two_likes_one
                    
def confirmCrushAndEmail(Person1, Person2):
    if isMatch(Person1, Person2): 
        sendEmail(Person1, Person2)
        return True
    else:
        return False

def sendEmail(Person1, Person2):
    SUBJECT = 'Mutual Crush Found!'
    MESSAGE = "Congradulations " + Person1.name + " and " + Person2.name + ", you both have a crush on each other!"
    EMAILS = [Person1.email, Person2.email]
    FROM = "crush@mit.edu"
    send_mail(SUBJECT, MESSAGE, FROM, EMAILS, fail_silently=False)
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('form is valid')
            person, created = Person.objects.get_or_create(
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email']
                )
            for i in range(Crush.num_allowed_crushes):
                crush_email = form.cleaned_data['Crush_email_%d' % (i+1)]
                crush_person, created = Person.objects.get_or_create(
                    email = crush_email
                )
                crush_person.name = '__no_name__ %s' % crush_email
                crush_person.save()
                crush = Crush(crusher=person, crushee=crush_person)
                crush.save()
            person.save()
            return HttpResponseRedirect('/admin')
        return HttpResponseRedirect('/register')

    else:
        form = RegisterForm()
        variables = RequestContext(request, {'form': form})
        return render_to_response('crush_connector/index.html', variables)

