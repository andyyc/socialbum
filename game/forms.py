from django import forms
from django.contrib.auth.models import User
from game.models import Game, BlackCard, WhiteCard, Submission

class GameForm(forms.Form):
    users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,queryset=User.objects.all())


class BlackCardModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.card.text
    
class WhiteCardModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.card.text

class BlackCardForm(forms.Form):
    black_card = BlackCardModelChoiceField(widget=forms.RadioSelect(),required=True,empty_label=None,queryset=BlackCard.objects.all())
    choice_list = forms.CharField(widget=forms.HiddenInput,max_length=64,required=False)

class WhiteCardForm(forms.Form):
    white_card = WhiteCardModelChoiceField(widget=forms.RadioSelect(), required=True,empty_label=None,queryset=WhiteCard.objects.all())

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
