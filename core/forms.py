import re
from django import forms
from .models import Order, Service, Review, Master
from django.core.exceptions import ValidationError

class OrderForm(forms.Form):
    client_name = forms.CharField(
        label='',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client Name'}),)
    phone = forms.CharField(
        label='',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '^(\+?7|8)\d{9,15}$'}),)
    comment = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment'})
    )
    master = forms.ModelChoiceField(
        label='Master',
        queryset=Master.objects.all(),
        required=False,
        initial=Master.objects.all().first(),
    )
    services = forms.ModelMultipleChoiceField(
        label='',
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs = {'placeholder': ''}),
    )
    def clean(self):
        cleaned_data = super().clean()
        client_name = cleaned_data.get('client_name', '')
        phone = cleaned_data.get('phone', '')

        if len(phone) + len(client_name) < 14:
            raise ValidationError('Имя + телефон не менее 14 символов :(((')
    def clean_phone(self):
        data = self.cleaned_data['phone']
        pattern = r'^(\+?7|8)\d{9,15}$'

        if not re.search(pattern, data):
            raise ValidationError(
                "Номер телефона должен быть в формате 8912433333 или +7912433333"
            )
        return data

class ReviewModelForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['client_name', 'text', 'master', 'photo', 'rating']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }