from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control input-lg',
															 'placeholder' : 'Username',
															 'title' : 'Your username is required!',
															 'required' : 'true'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control input-lg',
																 'placeholder' : 'Password',
																 'title' : 'Your password is required!',
																 'required' : 'true'}))
