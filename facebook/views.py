# Create your views here.
import urllib, cgi

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout

from socialbum import settings
from facebook.models import FacebookSession
from facebook import fb

def login(request):
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'code': request.GET['code'],
            }

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)

            response = cgi.parse_qs(urllib.urlopen(url).read())

            if not response:
                return HttpResponseRedirect('home')

            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = FacebookSession.objects.get_or_create(
                access_token=access_token,
            )[0]

            facebook_session.expires = expires
            facebook_session.save()

            user = auth.authenticate(token=access_token)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error}
    return render_to_response('login.html', template_context, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def contacts(request):
    try:
        fb_profile = FacebookSession.objects.get(user=request.user)
    except:
        raise Http404

    graph = fb.GraphAPI(fb_profile.access_token)
    fb_friends_list = graph.get_connections('me', 'friends')['data']
    fb_friends_list = sorted(fb_friends_list, key=lambda friend: friend['name'])

    only_fb_friends_list = []
    app_friends_list = []
    for fb_friends in fb_friends_list:
        fb_friends['picture_url'] = graph.request_url(fb_friends['id'] + '/picture')
        try:
            friend_profile = FacebookSession.objects.get(uid=fb_friends['id'])
        except FacebookSession.DoesNotExist:
            friend_profile = None

        if friend_profile is not None:
            app_friends_list.append(fb_friends)
        else:
            only_fb_friends_list.append(fb_friends)


    template_context = {'settings': settings,
                        'fb_friends_list': only_fb_friends_list,
                        'fb_profile' : fb_profile,
                        'app_friends_list': app_friends_list}

    return render_to_response('contacts.html', template_context, context_instance=RequestContext(request))