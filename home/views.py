# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
    #facebook_profile = request.user.get_profile().get_facebook_profile()
    facebook_profile = None
    return render_to_response('base.html',
                              { 'facebook_profile': facebook_profile },
                              context_instance=RequestContext(request))