# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from album.forms import AlbumForm
from album.models import Album
from django.contrib.auth.decorators import login_required
import json

@login_required
def create_album(request):
    print request
    if request.is_ajax() and request.method == 'POST':
        album_form = AlbumForm(request.POST)
        data = {}
        if album_form.is_valid():
            name = album_form.cleaned_data['name']
            Album.objects.create(name=name, owner=request.user)

            data['success'] = True
            data['name'] = name
        else:
            data['success'] = False
            data['form_errors'] = album_form.errors
        return HttpResponse(json.dumps(data), mimetype="application/json")

    raise Http404