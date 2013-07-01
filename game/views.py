from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from game.models import *
from game.forms import *
from facebook.views import get_friends_list
from facebook.models import FacebookSession

@login_required
def home(request):
    games = Game.objects.filter(users__id=request.user.id)
    template_context = {'games':games}
    return render_to_response('home.html', template_context, context_instance=RequestContext(request))

@login_required
def create(request):
    if request.method == 'POST':
        gf = GameForm(request.POST)
        if gf.is_valid():
            users = gf.cleaned_data['users']
            
            g = Game()
            g.save()

            for user in users:
                p = Player.objects.create(user=user, 
                                           game=g,
                                           points=0)
            p = Player.objects.create(user=request.user,
                                       game=g,
                                       points=0)
            
            #create black deck
            bc_tmpls = BlackCardTmpl.objects.all()
            for bc_tmpl in bc_tmpls:
                bc = BlackCard.objects.create(card=bc_tmpl,
                                              game=g,
                                              status='A')
                bc.save()
            #create turn
            turn = Turn.objects.create(game=g,
                                       num=0,
                                       judge=request.user)
            g.current_turn = turn
            g.save()
            
            return HttpResponseRedirect(reverse('game', kwargs={'game_id':g.id}))
        print gf
    else:
        gf = GameForm()

    try:
        fb_profile = FacebookSession.objects.get(user=request.user)
    except:
        raise Http404

    user_friends_list, user_friends_queryset, only_fb_friends_list = get_friends_list(fb_profile)

    gf.fields["users"].queryset = user_friends_queryset
    template_context = {'gf': gf,
                        'user_friends_list':user_friends_list,
                        'fb_friends_list':only_fb_friends_list}
    return render_to_response('create_game.html', template_context, context_instance=RequestContext(request))

def game(request, game_id):
    g = Game.objects.get(id=game_id)
    turn = g.current_turn
    
    if(turn.status == 0):
        if turn.judge == request.user:
            return pick_black_card(request, g)
        else:
            return show_point_table(request, g)
    elif(turn.status == 1):
        if turn.judge == request.user:
            return pick_winner(request, g)
        else:
            return pick_white_card(request, g)
    else:
        start_new_turn(request=request, game=g)
        return game(request, game_id)

def pick_black_card(request, game):
    bcf = None
    if request.method == 'POST':
        bcf = BlackCardForm(request.POST)
        if bcf.is_valid():
            #need to check that bc has not been used already
            bc = bcf.cleaned_data['black_card']
            choices_ids = bcf.cleaned_data['choice_list']
            BlackCard.objects.filter(id__in=choices_ids.split(',')).update(status='N')
            game.current_turn.status = 1
            game.current_turn.black_card = bc
            game.current_turn.save()
            return HttpResponseRedirect(reverse('game', kwargs={'game_id':game.id}))
    
    choices = game.blackcard_set.filter(status='A')[0:3]
        
    if not bcf:
        choices_ids = choices.values_list('id', flat=True)
        choices_ids = ','.join(str(i) for i in choices_ids)
        bcf = BlackCardForm(initial={'choice_list':choices_ids})
    
    bcf.fields["black_card"].queryset = choices

    template_context = {'bcf':bcf, 'game':game, 'topics':choices}
    return render_to_response('pick_black_card.html', 
                              template_context,
                              context_instance=RequestContext(request)) 

def show_point_table(request, game):
    players = Player.objects.filter(game=game)
    template_context = {'players':players}
    return render_to_response('point_table.html', 
                              template_context,
                              context_instance=RequestContext(request)) 

def pick_winner(request, game):
    return show_submissions(request, game, judge=True)
    """
    submissions = Submission.objects.filter(turn=game.current_turn)
    if request.method == 'POST':
        scf = SubmissionChoiceForm(request.POST)
        if scf.is_valid():
            sc = scf.cleaned_data['submission']
            game.current_turn.winner = sc
            game.current_turn.status = 2
            game.current_turn.save()
            p = Player.objects.get(game=game, user=sc.player.user)
            p.points += 1
            p.save()
            #start next turn
            start_new_turn(request, game)
            return show_point_table(request, game)
    else:
        scf = SubmissionChoiceForm()

    scf.fields["submission"].queryset = submissions
    template_context = {'scf':scf, 'game':game}
    return render_to_response('pick_winner.html',
                              template_context,
                              context_instance=RequestContext(request))
    """


def start_new_turn(request, game):
    turn = Turn(game=game,
                num=game.current_turn.num+1,
                status=0)
    users_list = list(game.users.values_list('id', flat=True))
    next_judge_id = users_list[(users_list.index(game.current_turn.judge.id)+1)%len(users_list)]
    turn.judge = game.users.get(id=next_judge_id)
    turn.save()
    game.current_turn = turn
    game.save()

def show_submissions(request, game, judge=False):
    # should check to see if user is judge

    sub_id = request.GET.get('sub_id', None)
    
    submissions = Submission.objects.filter(turn=game.current_turn)
    next_id = None
    prev_id = None
    if len(submissions) > 0:
        subs_list = list(submissions.values_list('id', flat=True))
        print subs_list
        if sub_id:
            submission = Submission.objects.get(id=sub_id)
            idx = subs_list.index(int(sub_id))
            next_id = subs_list[(idx+1)%len(subs_list)]
            prev_id = subs_list[(idx+1)%len(subs_list)]
        else:
            submission = submissions[0]
            next_id = subs_list[1%len(subs_list)]
            prev_id = subs_list[-1%len(subs_list)]
    else:
        submission = None
    
    clickX = []
    clickY = []
    clickDrag = []
    clickColor = []
    clickSize = []
    if submission:
        from django.utils.encoding import smart_str
        clickX = eval(submission.clickX)
        clickY = eval(submission.clickY)
        clickDrag = eval(submission.clickDrag)
        clickColor = eval(submission.clickColor)
        clickSize = eval(submission.clickSize)

        for i in xrange(len(clickX)):
            clickX[i] = smart_str(clickX[i])
            clickY[i] = smart_str(clickY[i])
            clickDrag[i] = smart_str(clickDrag[i])
            clickColor[i] = smart_str(clickColor[i])
            clickSize[i] = smart_str(clickSize[i])
        clickDrag = str(clickDrag).replace("'","")

    if judge:
        if request.method == 'POST':
            if submission != None:
                game.current_turn.winner = submission
                game.current_turn.status = 2
                game.current_turn.save()
                p = submission.player
                p.points += 1
                p.save()
                #start next turn
                start_new_turn(request, game)
                return show_point_table(request, game)

    template_context = {'clickX':clickX,
                        'clickY':clickY,
                        'clickDrag':clickDrag,
                        'clickColor':clickColor,
                        'clickSize':clickSize,
                        'submission':submission,
                        'next_id':next_id,
                        'prev_id':prev_id,
                        'judge':judge,
                        'game':game}
    return render_to_response('submissions.html',
                              template_context,
                              context_instance=RequestContext(request))

def pick_white_card(request, game):
    #check if user has already submitted a card
    p = Player.objects.get(user=request.user, game=game)
    try:
        s = Submission.objects.get(player=p, turn=game.current_turn)
        submitted = True
    except:
        submitted = False

    if submitted:
        return show_submissions(request, game)
    
    #hand = WhiteCard.objects.filter(game=game, user=request.user, turn=None, status='P')
    if request.method == 'POST' and request.is_ajax():
        rdict = {}
        clickX = request.POST.getlist('clickX[]')
        clickY = request.POST.getlist('clickY[]')
        clickDrag = request.POST.getlist('clickDrag[]')
        clickColor = request.POST.getlist('clickColor[]')
        clickSize = request.POST.getlist('clickSize[]')
        if clickX and clickY and clickDrag and clickColor and clickSize:
            Submission.objects.create(clickX=clickX,
                                      clickY=clickY,
                                      clickDrag=clickDrag,
                                      clickColor=clickColor,
                                      clickSize=clickSize,
                                      player=p,
                                      turn=game.current_turn)
            rdict.update({'status':'success'})
            return HttpResponse(simplejson.dumps(rdict))
        else:
            rdict.update({'status':'error'})
            return HttpResponse(simplejson.dumps(rdict))

    #wcf.fields["white_card"].queryset = hand
    template_context = {'game':game}
    return render_to_response('pick_white_card.html',
                              template_context,
                              context_instance=RequestContext(request))
