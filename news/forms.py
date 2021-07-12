from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=50)
    email = forms.EmailField(label='Email')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['editor','pub_date']
        widget = {
            'tags':forms.CheckboxSelectMultiple(),
        }