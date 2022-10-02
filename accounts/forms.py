from django import forms
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password, make_password



User = get_user_model()

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError('Username {} already exists'.format(username)) 



class LoginFrom(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
  
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Incorrect username or password')