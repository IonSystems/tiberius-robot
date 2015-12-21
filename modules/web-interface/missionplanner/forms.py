from django import forms
from .models import Mission

class MissionCreateForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['name', 'description', 'supported_platforms', 'estimated_duration', 'scheduled_start']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Apollo 13', 'type' :'text'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fly to the moon.', 'type' : 'text'}),
            'supported_platforms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'scheduled_start': forms.TextInput(attrs={'class': 'form-control'}),
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
