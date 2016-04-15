# -*- coding: utf-8 -*-

from django import forms

class TransferForm(forms.Form):
    def __init__(self, user_choices, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['users'].choices = user_choices

    users = forms.ChoiceField(required=False, widget=forms.Select, choices=())
    itn = forms.CharField(max_length=10)
    transfer_sum = forms.DecimalField(max_digits=12, decimal_places=2)
