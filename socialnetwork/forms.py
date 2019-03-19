from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from socialnetwork.models import *

MAX_UPLOAD_SIZE = 2500000

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, widget = forms.TextInput(attrs={'id':'id_username'}))
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput(attrs={'id':'id_password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            error = forms.ValidationError("Invalid username/password")
            raise error


        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20,  widget = forms.TextInput(attrs={'id':'id_username'}))
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput(attrs={'id':'id_password'}))
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm',  
                                 widget = forms.PasswordInput(attrs={'id':'id_confirm_password'}))
    
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput(attrs={'id':'id_email'}))
    first_name   = forms.CharField(max_length = 20,widget = forms.TextInput(attrs={'id':'id_first_name'}))
    last_name  = forms.CharField(max_length=20,widget = forms.TextInput(attrs={'id':'id_last_name'}))
    


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username
   

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', )

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture






