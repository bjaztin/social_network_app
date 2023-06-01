from django import forms
from django.forms import TextInput
from .models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  

class UserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
       
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'about', 'profile_pic')
        widgets = {
            'user': forms.HiddenInput(),
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Firstname'
                }),
            'last_name': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Lastname'
                }),
            'about': TextInput(attrs={
            'class': "form-control", 
            'style': 'max-width: 300px;', 'max-height:600;'
            'placeholder': 'about'
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('status', 'image_post')

    def __init__(self, *args, **kwargs):
        super(PostForm,self).__init__(*args, **kwargs)
        
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'status'
        self.fields['status'].label = ''
        self.fields['status'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['image_post'].widget.attrs['class'] = 'form-control-file'
        self.fields['image_post'].widget.attrs['placeholder'] = 'image_post'
        self.fields['image_post'].label = ''