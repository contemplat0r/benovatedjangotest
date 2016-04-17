# -*- coding: utf8 -*- 

import json
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from accounts.models import UserAccount
from accounts.forms import TransferForm
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_DOWN, getcontext

# Create your views here.


def process_transfer_request(user_name, itn, transfer_sum):
    process_result_message = ''
    user_account = UserAccount.objects.get(user__username=user_name)
    if transfer_sum <= user_account.ammount:
        recipients = UserAccount.objects.exclude(
            user__username=user_name).filter(itn=itn)
        recipients_num = recipients.count()
        if recipients_num > 0:
            transfer_to_one_recipient = Decimal((transfer_sum / recipients_num).quantize(Decimal('.00'), rounding=ROUND_HALF_DOWN))
            if transfer_to_one_recipient * recipients_num > transfer_sum:
                transfer_to_one_recipient = Decimal((transfer_sum / recipients_num).quantize(Decimal('.00'), rounding=ROUND_DOWN))

            user_account.ammount -= transfer_to_one_recipient * recipients_num
            for recipient in recipients:
                recipient.ammount += transfer_to_one_recipient
                recipient.save()
            user_account.save()

            process_result_message = 'Transfered to %s accounts for %s. Account balance %s' % (str(recipients_num), str(transfer_to_one_recipient), str(user_account.ammount))

        else:
            process_result_message = 'None recipients with that identifier: %s' % itn
    else:
        process_result_message = 'Transfer sum exceed ammount of funds in account'

    return process_result_message


def transfer(request):
    user_accounts = UserAccount.objects.all()
    user_names = [user_account.user.username for user_account in user_accounts]
    names_choice_set = [(name, name) for name in user_names]

    transfer_form = TransferForm(names_choice_set)

    transfer_result_message = None
   
    if request.method == 'POST' and request.is_ajax():
        transfer_form = TransferForm(names_choice_set, request.POST)
        errors = None
        success = True
        if transfer_form.is_valid():
            selected_user_name = transfer_form.cleaned_data.get('users')
            itn = transfer_form.cleaned_data.get('itn')
            transfer_sum = transfer_form.cleaned_data.get('transfer_sum')
            transfer_result_message = process_transfer_request(
                selected_user_name, itn, transfer_sum)
        else:
            transfer_result_message = 'Data is invalid'
            errors = json.loads(transfer_form.errors.as_json())
            success = False
        return JsonResponse({'success' : success, 'transferResultMessage' : transfer_result_message, 'errors' : errors})
    elif request.method == 'GET':
        transfer_form = TransferForm(names_choice_set)
    else:
        transfer_form = TransferForm(names_choice_set)
        transfer_result_message = 'Incorrect request method'

    context = {'transfer_form' : transfer_form}
    context.update(csrf(request))
    #return render(request, 'accounts/transfer.html', context)
    return render_to_response('accounts/transfer.html', context)
