from models import *
from django.core.mail import send_mail
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from crush_connector.models import Person, Crush, RefreshDates
from crush_connector.forms import RegisterForm
from datetime import datetime, timedelta

def isMatch(Person1, Person2):
    crushes = Crush.objects.filter(active=True)
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
        # if the person has not yet been notified about Crush, then notify them!
        try:
            notified = PersonBeenNotified.objects.get(person=Person2)
        except:
            sendEmailNoMatch(Person2)
            notified = PersonBeenNotified(person=Person2)
            notified.save()
        return False

def sendEmail(Person1, Person2):
    SUBJECT = 'Mutual Crush Found!'
    MESSAGE = "Congratulations " + Person1.name + " and " + Person2.name + ", you both have a crush on each other!"
    EMAILS = [Person1.email, Person2.email]
    FROM = "crush@mit.edu"
    send_mail(SUBJECT, MESSAGE, FROM, EMAILS, fail_silently=False)

def sendEmailNoMatch(Person2):
    SUBJECT = 'An anonymous MIT student has a crush on you...'
    MESSAGE = '''Dear %s,

An anonymous MIT student has a crush on you. Go on http://crush.mit.edu, fill out a list of people you have a crush on, and see if there\'s a match!'''
    EMAILS = [Person2.email]
    FROM = 'crush@mit.edu'
    send_mail(SUBJECT, MESSAGE, FROM, EMAILS, fail_silently=False)

def sendVerificationEmail(Person):
    SUBJECT = "MIT Crush Verification"
    LINK = "http://18.181.0.46:4040/register?email=%s&key=%s" %(Person.email, Person.SecretKey)
    MESSAGE = "You are receiving this email because you made a crush request on MIT Crush Connector." + LINK  + " If this action was not done by you, please disregard this email and do not click the above link"
    EMAILS = [Person.email]
    FROM = "crush@mit.edu"
    send_mail(SUBJECT, MESSAGE, FROM, EMAILS, fail_silently=False)

def submit(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        print('form is valid')
        if not 'REDIRECT_SSL_CLIENT_S_DN_Email' in request.META:
            return render_to_response('crush_connector/need_certificate.html')
        person = Person.objects.get(
            email = request.META['REDIRECT_SSL_CLIENT_S_DN_Email'] 
            )
        num_allowed = person.num_allowed_crushes
        if num_allowed < 0:
            num_allowed = Crush.num_allowed_crushes

        num_submitted = 0
        for i in range(Crush.num_allowed_crushes):
            crush_email = form.cleaned_data['Crush_email_%d' % (i+1)]
            if crush_email != '':
                num_submitted += 1

        num_left = num_allowed - person.num_crushes_used

        crushes = Crush.objects.filter(crusher=person).order_by('-timestamp')
        crushees = [crush.crushee for crush in crushes]
        next_refresh = RefreshDates.objects.filter(date__gte = datetime.today()).order_by('date')[0]

        variables = RequestContext(request, {
                'num_left': num_left,
                'num_allowed': num_allowed,
                'num_used': person.num_crushes_used,
                'refresh_date': next_refresh,
                'crushees': crushees
            })
    
        if num_submitted > num_left:
            last_submission = crushes[0].timestamp
            last_refresh = RefreshDates.objects.filter(date__lte = datetime.today()).order_by('-date')[0]
            if last_refresh.date > last_submission.date():
                for crush in crushes:
                    crush.active = False
                    crush.save()
                person.num_crushes_used = 0
            else:
                # too many, not allowed to submit this many crushes
                # throw error page, tell them to go back and submit fewer and wait til refresh date to submit more
                return render_to_response('crush_connector/over_limit.html', variables)
        
        for i in range(Crush.num_allowed_crushes):
            crush_email = form.cleaned_data['Crush_email_%d' % (i+1)]
            if crush_email == '':
                continue
            crush_person, created = Person.objects.get_or_create(
                email = crush_email
                )
            if created:
                print('creating new person for the crush')
                crush_person.name = '__no_name__  %s' % crush_email
                crush_person.save()
            crush = Crush(crusher=person, crushee=crush_person)
            crush.save()
            person.num_crushes_used += 1
            person.save()
            if confirmCrushAndEmail(person, crush_person):
                print('match! check your email')
        num_left = num_left - num_submitted

        variables = RequestContext(request, {
                'num_left': num_left,
                'num_allowed': num_allowed,
                'num_used': person.num_crushes_used,
                'refresh_date': next_refresh,
                'crushees': crushees
            })

        return render_to_response('crush_connector/validate.html', variables)
    else:        
        variables = RequestContext(request, {'form': form})
        return render_to_response('crush_connector/connect.html', variables)

def index(request):
    form = RegisterForm()
    variables = RequestContext(request, {'form': form,})
    return render_to_response('crush_connector/connect.html', variables)

def about(request):
    return render_to_response('crush_connector/about.html')

def success(request):
    return render_to_response('crush_connector/validate.html')

def getlabels(request):
    matching = quickSearch(request.GET.get('term', 'oawiejfoawiejf'))
    list = "["
    first = True
    for person in matching:
        if (not first):
            list += " , "
        first = False
        list += '{"label": "' + person + '", "value": "' + person.split(" ")[-1] + '"}'
    list += "]"
    return HttpResponse(list)

def clearMiddleNames(request):
    persons = Person.objects.all()
    for person in persons:
        name_list = person.name.split(" ")
        if len(name_list) >= 2:
            person.name = name_list[0] + " " + name_list[-1]
        elif len(name_list) == 1:
            person.name = name_list[0]
        else:
            person.name = "Invalid Name"
        person.save()
    return HttpResponse("Done")

def getEmails(request):
    persons = Person.objects.all()
    list = '['
    first = True
    for person in persons:
        if (not first):
            list += ","
        first = False
        list += '"' + person.email +'"'
    list += ']'
    return HttpResponse(list)
            
def quickSearch(name):
    persons = Person.objects.all()
    list = []
    for person in persons:
        list.append(person.name + " " + person.email)
    matching = [s for s in list if name in s]
    return matching
    
def getnames(request):
    return render_to_response('crush_connector/names.json')

