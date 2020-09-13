from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = request.user.username
    class Meta:
        model = Comment
        fields = ('name','contents',)
        labels = { 'contents': (''),}
        widgets = {'name': forms.HiddenInput()}
'''
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',   
            'email', 
            'password1', 
            'password2', 
            ]
'''
class PasswordResetForm(forms.Form):
    email = forms.CharField(label='E-mail:',max_length=50)

class PasswordChangeForm(forms.Form):
    old_pass = forms.CharField(label='Old password', widget=forms.PasswordInput)
    new_pass1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_pass2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput)
    
    def __init__(self, request, *args, **kwargs):
       super(PasswordChangeForm, self).__init__(*args, **kwargs)
       self.user = request.user 

    def clean_old_pass(self):
        old_pass = self.cleaned_data.get('old_pass')
        success = self.user.check_password(old_pass)
        if not success:
            raise ValidationError("Wrong password")
        return old_pass

    def clean_new_pass2(self):
        new_pass1 = self.cleaned_data.get('new_pass1')
        new_pass2 = self.cleaned_data.get('new_pass2')

        if new_pass1 and new_pass2 and new_pass1 != new_pass2:
            raise ValidationError("Password don't match")
        return new_pass2

class SignUpForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        print("\n\nkurwa")
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        print("\n\nkurwa")
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        print("\n\nkurwa")
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        print("\n\nkurwasave")
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            is_active = False,
        )
        return user