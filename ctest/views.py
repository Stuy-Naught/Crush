from django.http import HttpResponse
from django.core.mail import send_mail
def index(request):
    #send_mail('testing email', 'here is a message', 'crush@mit.edu', ['wmh1993@gmail.com'], fail_silently=False)
    
    return HttpResponse("Hello world.")



    
