from shop.models import Comment, StarRating, Product
from django.db import models
from django import forms
from django.forms import (ModelForm, TextInput, DateTimeInput, 
                          PasswordInput, EmailInput)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["user", "product", "star_rating", "description", "taste_rating", "price_rating", "representability_rating"]


class StarRatingForm(ModelForm):
    class Meta:
        model = StarRating
        fields = ["star_1", "star_2", "star_3", "star_4", "star_5", "product"]


class ProductStarRatingUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['star_rating']
