from django import forms
from django.forms import widgets

from otzovikapp.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти",
                             widget=widgets.TextInput(attrs={'class': 'form-control'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['author', 'product', 'is_moderated']
