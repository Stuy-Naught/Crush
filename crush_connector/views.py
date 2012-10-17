from models import *
from django.http import HttpResponse
from django.core.mail import send_mail

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
    
