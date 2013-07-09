# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from facebook.models import FacebookSession
from album.forms import AlbumForm
from django.contrib.auth.decorators import login_required

def home(request):

    try:
        #facebook_profile = request.user.facebook_session.get_facebook_profile()
        facebook_profile = FacebookSession.objects.get(user=request.user)
    except:
        facebook_profile = None

    if facebook_profile !=None:
        album_form = AlbumForm();
        albums = request.user.album_set.all()
    else:
        album_form = None
        albums = None

    return render_to_response('home.html',
                              { 'facebook_profile': facebook_profile,
                                'album_form': album_form,
                                'albums': albums },
                              context_instance=RequestContext(request))