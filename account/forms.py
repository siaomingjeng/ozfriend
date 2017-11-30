from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    verify = forms.CharField(max_length=6, widget=forms.TextInput(
            attrs={'class': 'verification'}))    
