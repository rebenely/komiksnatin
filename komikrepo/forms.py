from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
    description = forms.CharField(help_text='Say something about yourself!');
    class Meta:
        model = User
        fields = ('username', 'description', 'password1', 'password2', )

class EditForm(forms.Form):
    description = forms.CharField(required=False);
    username = forms.CharField(help_text='Say something about yourself!');
    oldpassword = forms.CharField(help_text='Say something about yourself!');
    password1 = forms.CharField(help_text='Say something about yourself!');
    password2 = forms.CharField(help_text='Say something about yourself!');

    class Meta:
        fields = ('username', 'description', 'oldpassword' ,'password1', 'password2', )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        old_password = cleaned_data.get("oldpassword")
        new_password1 = cleaned_data.get("password1")
        new_password2 = cleaned_data.get("password2")
        user = authenticate(username=username, password=old_password)
        if not user:
            raise forms.ValidationError(
                "Wrong password!"
            )

        if old_password == new_password1:
            raise forms.ValidationError(
                "New password must not be old password!"
            )
        if new_password1 and len(new_password1) < 5:
            raise forms.ValidationError(
                "Password must be at least 5 characters!"
            )
        if new_password1 and new_password2 and new_password2 != new_password1:
            raise forms.ValidationError(
                "New password does not match!"
            )
