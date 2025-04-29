from django import forms
from .models import Recipe
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
import os

class RecipeForm(forms.ModelForm):
    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Or paste image URL here'
        })
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'cuisine', 'meal_type', 'image', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief description of the recipe'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'List ingredients, one per line'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Step-by-step cooking instructions'}),
            'cuisine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Italian, Indian'}),
            'meal_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Breakfast, Dinner'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:  # Limit to 5MB
            raise forms.ValidationError("Image file too large (max 5MB).")
        return image

    def clean_image_url(self):
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            try:
                validate = URLValidator()
                validate(image_url)
                # Try to open the URL to check if it's accessible
                response = urlopen(image_url)
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    raise ValidationError("URL must point to an image file.")
            except (URLError, ValidationError):
                raise forms.ValidationError("Invalid URL or cannot access the image.")
        return image_url

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if not image and not image_url:
            raise forms.ValidationError("Please provide either an image file or an image URL.")
        if image and image_url:
            raise forms.ValidationError("Please provide either an image file or an image URL, not both.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_url = self.cleaned_data.get('image_url')

        if image_url and not self.cleaned_data.get('image'):
            try:
                response = urlopen(image_url)
                if response.getcode() == 200:
                    # Get the filename from the URL
                    filename = os.path.basename(urlparse(image_url).path)
                    if not filename:
                        filename = 'downloaded_image.jpg'
                    
                    # Save the image
                    instance.image.save(
                        filename,
                        ContentFile(response.read()),
                        save=False
                    )
            except URLError:
                raise forms.ValidationError("Could not download the image from the provided URL.")

        if commit:
            instance.save()
        return instance

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

