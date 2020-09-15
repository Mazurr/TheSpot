from .models import Comment, Post, Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

choices = Category.objects.all().values_list('name', 'name')

class PostForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['author'].widget.attrs['readonly'] = True
        self.initial['author'] = request.user.pk
    class Meta:
        model = Post
        fields = ('title', 'slug','author','content', 'category', 'status')
        widgets = { 'category': forms.Select(choices = choices, attrs={'class': 'form-control'}), 
                    'author': forms.HiddenInput(),}

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content', 'category','status')
        widgets = { 'title': forms.TextInput(attrs={'class': 'form-control'}), 'category': forms.Select(choices = choices, attrs={'class': 'form-control'}),
                    'status': forms.Select(attrs={'class': 'form-control'})}

class CommentForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['name'].initial = request.user.username
    class Meta:
        model = Comment
        fields = ('name','contents',)
        labels = { 'contents': (''),}
        widgets = {'name': forms.HiddenInput()}

class PasswordResetForm(forms.Form):
    email = forms.CharField(label='E-mail:',max_length=50)

class PasswordChangeForm(forms.Form):
    old_pass = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_pass1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_pass2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
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

class EmailChangeForm(forms.Form):
    password = forms.CharField(label='Account password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_email = forms.EmailField(label='New Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    def __init__(self, request, *args, **kwargs):
       super(EmailChangeForm, self).__init__(*args, **kwargs)
       self.user = User.objects.get(username=request.user.username) 

    def clean_password(self):
        passw = self.cleaned_data.get('password')
        success = self.user.check_password(passw)
        if not success:
            raise ValidationError("Wrong password")
        return passw

    def clean_new_email(self):
        email = self.cleaned_data.get('new_email')
        email_list = User.objects.filter(is_active=True).values_list('email', flat=True)
        if email in email_list:
            raise ValidationError("Email is used")
        return email

class DeleteUserForm(forms.Form):
    passw = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, request, *args, **kwargs):
       super(DeleteUserForm, self).__init__(*args, **kwargs)
       self.user = request.user 

    def clean_passw(self):
        passw = self.cleaned_data.get('passw')
        success = self.user.check_password(passw)
        if not success:
            raise ValidationError("Wrong password")
        return passw

class SignUpForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Enter email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            is_active = False,
        )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def __init__(self, request, *args, **kwargs):
       super(LoginForm, self).__init__(*args, **kwargs)