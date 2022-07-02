from django.forms import ModelForm
from .models import Room, User, Product
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']


class AddToCart(forms.Form):
    quantity = forms.IntegerField()


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    stripe_token = forms.CharField(max_length=255)
