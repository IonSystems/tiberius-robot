from django import forms
from .models import Mission
from .models import Task
from .models import Robot


class MissionCreateForm(forms.ModelForm):
    scheduled_start = forms.DateTimeField(
        label='buy date', input_formats=['%m/%d/%Y %H:%M %p'])
    scheduled_start.widget = forms.TextInput(attrs={'class': 'form-control'})

    def __init__(self, user, *args, **kwargs):
        super(MissionCreateForm, self).__init__(*args, **kwargs)
        self.creator = user

    class Meta:
        model = Mission
        fields = ['name', 'description',
                  'supported_platforms', 'scheduled_start']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apollo 13', 'type': 'text'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fly to the moon.', 'type': 'text'}),
            'supported_platforms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            #'scheduled_start': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class MissionCreateForm(forms.Form):
#     mission_name = forms.CharField(label='Mission Name', max_length=50)
#     mission_name.widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Apollo 13', 'type' :'text'})
#
#     mission_description = forms.CharField(label='Mission Description', max_length=500)
#     mission_description.widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fly to the moon.', 'type' : 'text'})
#
#     supported_platforms = forms.MultipleChoiceField(label='Supported Platforms',choices = (('FR', 'Freshman'),('SO', 'Sophomore')))
#     supported_platforms.widget = forms.SelectMultiple(attrs={'class': 'form-control'})

from django.forms import ModelForm
from django import forms
from fleet.models import Robot


class SendTaskRequestForm(forms.Form):
    task = forms.ModelChoiceField(label="Task", queryset=Task.objects.all(),widget=forms.Select(attrs={'class':'form-control input-sm'}))
    platform = forms.ModelChoiceField(label="Platform", queryset=Robot.objects.all(),widget=forms.Select(attrs={'class':'form-control input-sm'}))
