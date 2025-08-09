from django import forms
from .models import Order, Service, Review, Master
from django.core.exceptions import ValidationError

class OrderForm(forms.Form):
    client_name = forms.CharField(label='Client Name', max_length=100)
    phone = forms.CharField(label='Phone Number', max_length=100)
    comment = forms.CharField(label='Comment', widget=forms.Textarea)
    master = forms.ModelChoiceField(
        label='Master',
        queryset=Master.objects.all(),
        required=False
    )
    service = forms.ModelMultipleChoiceField(
        label='Service',
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
            "master": forms.Select(attrs={'class': 'form-control'}),
            "service": forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }