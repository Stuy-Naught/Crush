from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

def custom_403(request):
    return render_to_response('crush_connector/error.html')

def custom_404(request):
    return render_to_response('crush_connector/error.html')

def custom_500(request):
    return render_to_response('crush_connector/error.html')
