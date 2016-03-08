from django.forms import ModelForm
from django import forms
from fleet.models import Robot


class ChangeRobotForm(forms.Form):
    name = forms.ModelChoiceField(label="Robot Name", queryset=Robot.objects.all(),widget=forms.Select(attrs={'class':'form-control input-sm'}))
