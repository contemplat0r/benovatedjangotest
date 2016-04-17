# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms


def validate_itn(value):
    if len(value) != 10 and len(value) != 12:
        raise ValidationError(('%(value)s length not equal 10 or 12'), params={'value' : value},)
    if not value.isdigit():
        raise ValidationError(('all inputed symbols must be digits'),)



class TransferForm(forms.Form):
    def __init__(self, user_choices, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['users'].choices = user_choices

    users = forms.ChoiceField(required=False, widget=forms.Select, choices=())
    itn = forms.CharField(max_length=10, validators=[validate_itn])
    transfer_sum = forms.DecimalField(max_digits=12, decimal_places=2)
