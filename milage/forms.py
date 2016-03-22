from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserCreationForm(UserForm):
    password_again = forms.CharField(widget=forms.PasswordInput())