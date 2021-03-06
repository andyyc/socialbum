from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from game.models import Game, GameTopic, Player, Topic, Turn, Submission
from game.forms import GameTopicForm, GameForm, SubmissionChoiceForm
from facebook.views import get_friends_list
from facebook.models import FacebookSession

import json

NUM_TOPIC_CHOICES = 3

@login_required
def games(request):
    print request.user
    active_games = Game.objects.filter(users__id=request.user.id).filter(completed=False)
    completed_games = Game.objects.filter(users__id=request.user.id).filter(completed=True)
    template_context = {'games':active_games,
                        'completed_games':completed_games}
    return render_to_response('games.html', template_context, context_instance=RequestContext(request))

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
            

            topics = Topic.objects.filter(deleted=False).order_by('?')
            for topic in topics:
                game_topic = GameTopic.objects.create(topic=topic,
                                                        game=g)
            #create turn
            turn = Turn.objects.create(game=g,
                                       num=1,
                                       judge=request.user)
            g.current_turn = turn
            g.save()
            
            return HttpResponseRedirect(reverse('game', kwargs={'game_id':g.id}))
    else:
        gf = GameForm()

    try:
        fb_profile = FacebookSession.objects.get(user=request.user)
    except FacebookSession.DoesNotExist:
        raise Http404

    user_friends_list, user_friends_queryset, only_fb_friends_list = get_friends_list(fb_profile)

    gf.fields["users"].queryset = user_friends_queryset
    template_context = {'gf': gf,
                        'user_friends_list':user_friends_list,
                        'fb_friends_list':only_fb_friends_list}
    return render_to_response('create_game.html', template_context, context_instance=RequestContext(request))

@login_required
def game(request, game_id):
    try:
        g = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        raise Http404

    if g.completed:
        return show_point_table(request, g)

    turn = g.current_turn

    if turn.status == 0:
        if turn.judge == request.user:
            return choose_topic(request, g)
        else:
            return show_point_table(request, g)
    elif turn.status == 1:
        if turn.judge == request.user:
            return HttpResponseRedirect(reverse('submission', kwargs={
                'game_id':game_id,
                'turn_id':g.current_turn.id,
                'page':0,
            }))
        else:
            return draw(request, g)
    else:
        start_new_turn(request=request, game=g)
        return game(request, game_id)

@login_required
def choose_topic(request, game):
    #check that person making request is the current turn's judge

    if request.method == 'POST':
        game_topic_form = GameTopicForm(request.POST)
        if game_topic_form.is_valid():
            #need to check that game topic has not been used already
            """
            game_topic_choices = game.gametopic_set.filter(used=False)[0:3]
            for game_topic_choice in game_topic_choices:
                game_topic_choice.used = True
                game_topic_choice.save()
            """

            game_topic_id = game_topic_form.cleaned_data['game_topic']
            try:
                game_topic = GameTopic.objects.get(id=game_topic_id)
            except GameTopic.DoesNotExist:
                game_topic = None

            if game_topic:
                game_topic.used = True
                game_topic.save()
                game.current_turn.status = 1
                game.current_turn.game_topic = game_topic
                game.current_turn.save()
                return HttpResponseRedirect(reverse('game', kwargs={'game_id':game.id}))
    else:
        game_topic_form = GameTopicForm()

    game_topics = game.gametopic_set.filter(used=False)
    selected_game_topics = select_three_random(game.current_turn.num, list(game_topics))
    template_context = {'game_topic_form':game_topic_form,
                        'game':game,
                        'game_topics':selected_game_topics}

    return render_to_response('choose_topic.html',
                              template_context,
                              context_instance=RequestContext(request)) 

#This function takes a turn number and a list of game topics and return three "random" topics
#Random meaning the results will be different for each turn number, but the same for a given number
def select_three_random(turn_num, game_topics):
    num_game_topics = len(game_topics)

    if num_game_topics < NUM_TOPIC_CHOICES :
        return game_topics

    selected_game_topics = []
    for i in xrange(0,NUM_TOPIC_CHOICES):
        idx = some_hash(turn_num + i, num_game_topics-i)
        selected_game_topics.append(game_topics[idx])
        game_topics[idx] = game_topics[num_game_topics - i - 1]
    return selected_game_topics

def some_hash(num, buckets):
    return num*2654435761 % buckets;

def show_point_table(request, game):
    players = game.player_set.all()
    turns = game.turn_set.filter(status=2)

    if turns:
        prev_turn = turns.order_by('id').reverse()[0]
    else:
        prev_turn = None

    template_context = {'players':players,
                        'turns':turns,
                        'prev_turn':prev_turn,
                        'game':game}
    return render_to_response('points_table.html',
                              template_context,
                              context_instance=RequestContext(request)) 

def pick_winner(request, game):
    is_judge = game.current_turn.judge == request.user
    sub_choice_form = None
    submissions = Submission.objects.filter(turn=game.current_turn)

    if is_judge:
        if request.method == 'POST':
            sub_choice_form = SubmissionChoiceForm(request.POST)
            if sub_choice_form.is_valid():
                submission = sub_choice_form.cleaned_data['submission']
                game.current_turn.winner = submission
                game.current_turn.status = 2
                game.current_turn.save()
                player = submission.player
                player.points += 1
                player.save()
                if player.points >= 3:
                    game.completed = True
                    game.winner = player
                    game.save()
                else:
                    start_new_turn(request, game)

                return HttpResponseRedirect(reverse('game', kwargs={'game_id':game.id}))
        else:
            sub_choice_form = SubmissionChoiceForm()

        sub_choice_form.fields["submission"].queryset = submissions

    return show_submissions(request, game, is_judge, sub_choice_form)


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

@login_required
def show_submissions(request, game, is_judge=False, sub_choice_form=None):
    # should check to see if user is judge
    submissions = Submission.objects.filter(turn=game.current_turn)

    if not submissions.exists():
        return show_point_table(request, game)

    from django.core import serializers
    submissions_json = serializers.serialize('json',
                                            submissions,
                                            fields=('id', 'clickX', 'clickY', 'clickDrag', 'clickSize', 'clickColor'))

    template_context = {'judge':is_judge,
                        'game':game,
                        'turn':game.current_turn,
                        'submissions':submissions,
                        'submissions_json':submissions_json,
                        'sub_choice_form':sub_choice_form}

    return render_to_response('submissions.html',
                              template_context,
                              context_instance=RequestContext(request))

def turn(request, game_id, turn_id):

    try:
        game = Game.objects.get(id=game_id)
    except:
        raise Http404

    try:
        turn = Turn.objects.get(id=turn_id)
    except:
        raise Http404

    if turn == game.current_turn and not game.completed:
        return HttpResponseRedirect(reverse('game', kwargs={'game_id':game_id}))

    return submission(request, game_id, turn_id, 0)

@login_required
def submission(request, game_id, turn_id=None, page=0):

    page = int(page)

    try:
        game = Game.objects.get(id=game_id)
    except:
        raise Http404

    if not turn_id:
        turn = game.current_turn
    else:
        try:
            turn = Turn.objects.get(id=turn_id)
        except:
            raise Http404

    submissions = turn.submission_set.all()

    if not submissions:
        return show_point_table(request, game)

    try:
        submission = submissions[page]
    except:
        raise Http404

    is_judge = turn.judge == request.user and turn == game.current_turn and turn.status == 1
    sub_choice_form = None

    if is_judge:
        if request.method == 'POST':
            sub_choice_form = SubmissionChoiceForm(request.POST)
            sub_choice_form.fields["submission"].queryset = submissions

            if sub_choice_form.is_valid():
                submission = sub_choice_form.cleaned_data['submission']
                game.current_turn.winner = submission
                game.current_turn.status = 2
                game.current_turn.save()
                player = submission.player
                player.points += 1
                player.save()

                if player.points == 4:
                    game.completed = True
                    game.winner = player
                    game.save()
                else:
                    start_new_turn(request, game)

                return HttpResponseRedirect(reverse('game', kwargs={'game_id':game.id}))
        else:
            sub_choice_form = SubmissionChoiceForm(initial={
                'submission':submission,
            })

        sub_choice_form.fields["submission"].queryset = submissions

    prev = None
    has_prev = False

    if page > 0:
        prev = page-1
        has_prev = True

    next = None
    has_next = False

    if page < len(submissions)-1:
        next = page+1
        has_next = True


    from django.core import serializers
    submission_json = serializers.serialize('json',
                                            [submission,],
                                            fields=('id', 'clickX', 'clickY', 'clickDrag', 'clickSize', 'clickColor'))

    show_turn_nav = True
    #force user to make selection, no browsing
    if turn == game.current_turn and turn.status != 2 and request.user == game.current_turn.judge:
        show_turn_nav = False

    turns = game.turn_set.all()

    template_context = {'judge':is_judge,
                        'game':game,
                        'turn':turn,
                        'submission':submission,
                        'submission_json':submission_json,
                        'show_turn_nav':show_turn_nav,
                        'turns':turns,
                        'prev':prev,
                        'next':next,
                        'has_next':has_next,
                        'has_prev':has_prev,
                        'sub_choice_form':sub_choice_form,
                        'page':page,
                        }

    return render_to_response('submission.html',
                          template_context,
                          context_instance=RequestContext(request))

@login_required
def draw(request, game):
    #check if user has already submitted a card
    try:
        p = Player.objects.get(user=request.user, game=game)
    except Player.DoesNotExist:
        raise Http404

    try:
        Submission.objects.get(player=p, turn=game.current_turn)
        submitted = True
    except Submission.DoesNotExist:
        submitted = False

    if submitted:
        return submission(request, game.id, game.current_turn.id)

    submit_error = False
    if request.method == 'POST':
        clickX = request.POST.get('clickX')
        clickY = request.POST.get('clickY')
        clickDrag = request.POST.get('clickDrag')
        clickColor = request.POST.get('clickColor')
        clickSize = request.POST.get('clickSize')
        if clickX and clickY and clickDrag and clickColor and clickSize:
            Submission.objects.create(clickX=clickX,
                                      clickY=clickY,
                                      clickDrag=clickDrag,
                                      clickColor=clickColor,
                                      clickSize=clickSize,
                                      player=p,
                                      turn=game.current_turn)
            return HttpResponseRedirect(reverse('game', kwargs={'game_id':game.id}))
        else:
            submit_error = True

    template_context = {'game':game,
                        'submit_error':submit_error}

    return render_to_response('draw.html',
                              template_context,
                              context_instance=RequestContext(request))
