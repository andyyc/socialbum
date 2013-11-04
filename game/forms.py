from django import forms
from django.contrib.auth.models import User
from game.models import Game, GameTopic, Submission

class GameForm(forms.Form):
    users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,queryset=User.objects.all())

class GameTopicChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.topic.text

class GameTopicForm(forms.Form):
    game_topic = forms.IntegerField(widget=forms.HiddenInput,required=True)

class SubmissionChoiceForm(forms.Form):
    submission = forms.ModelChoiceField(widget=forms.RadioSelect(), required=True,empty_label=None,queryset=Submission.objects.all())
