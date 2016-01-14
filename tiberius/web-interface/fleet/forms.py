from django import forms
from .models import Robot

class RobotForm(forms.ModelForm):
    #scheduled_start = forms.DateTimeField(label='buy date', input_formats=['%m/%d/%Y %H:%M %p'])
    #scheduled_start.widget = forms.TextInput(attrs={'class': 'form-control'})
    class Meta:
        model = Robot
        fields = ['name', 'ip_address', 'mac_address', 'weight', 'capacity', 'owner', 'permitted_users', 'control_enabled', 'autonomy_enabled', 'object_detection_enabled', 'database_enabled', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Apollo 13', 'type' :'text'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fly to the moon.', 'type' : 'text'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fly to the moon.', 'type' : 'text'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fly to the moon.', 'type' : 'text'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fly to the moon.', 'type' : 'text'}),
            'supported_platforms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            #'scheduled_start': forms.TextInput(attrs={'class': 'form-control'}),
        }
