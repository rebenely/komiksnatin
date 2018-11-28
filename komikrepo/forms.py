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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        new_password1 = cleaned_data.get("password1")
        new_password2 = cleaned_data.get("password2")

        if username and len(username) > 20:
            raise forms.ValidationError(
                "Username must be less than 20 chars!"
            )
        if username and len(username) < 5:
            raise forms.ValidationError(
                "Username must be greater than 5 chars!"
            )
        if new_password2 and new_password1 and len(new_password2) > 20 and len(new_password1) > 20:
            raise forms.ValidationError(
                "Password must be less than 20 chars!"
            )

class EditForm(forms.Form):
    description = forms.CharField(required=False);
    username = forms.CharField(help_text='Say something about yourself!');
    oldpassword = forms.CharField(help_text='Say something about yourself!');
    password1 = forms.CharField(help_text='Say something about yourself!', required=False);
    password2 = forms.CharField(help_text='Say something about yourself!', required=False);

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
        if new_password1 and new_password2:
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
        if new_password1 and not new_password2:
            raise forms.ValidationError(
                "Must retype new password!"
            )
        if new_password2 and not new_password1:
            raise forms.ValidationError(
                "Must retype new password!"
            )


class ReviewForm(forms.Form):
    comment = forms.CharField(required=False, max_length=500);
    rating = forms.IntegerField()

    class Meta:
        fields = ('comment', 'rating' )

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get("rating")
        comment = cleaned_data.get("comment")

        print(comment)
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Must be in the range 1-5!")

class ListCreateForm(forms.Form):
    title = forms.CharField(required=True, max_length=100);
    description = forms.CharField(required=True, max_length=500);

    class Meta:
        fields = ('title', 'description')

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
