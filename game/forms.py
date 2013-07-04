from django import forms
from django.contrib.auth.models import User
from game.models import Game, GameTopic, Submission

class GameForm(forms.Form):
    users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,queryset=User.objects.all())

class GameTopicChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.topic.text

class GameTopicForm(forms.Form):
    game_topic = GameTopicChoiceField(widget=forms.RadioSelect(),required=True,empty_label=None,queryset=GameTopic.objects.all())

"""
class SubmissionForm(forms.Form):
    clickX = forms.RegexField(regex='^[\d,]+$', required=False)
    clickY = forms.MultipleChoiceField(required=False)
    clickSize = forms.MultipleChoiceField(required=False)
    clickColor = forms.MultipleChoiceField(required=False)
    clickDrag = forms.MultipleChoiceField(required=False)
"""

class SubmissionChoiceForm(forms.Form):
    submission_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
