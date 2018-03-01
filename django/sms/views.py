from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def send_sms(request):
    result = 0
    if request.method == 'POST':

        phone_num1 = request.POST.get('phone_number1')
        phone_num2 = request.POST.get('phone_number2')
        text = request.POST.get('text')

        # set api key, api secret
        api_key = settings.SMS_API_KEY
        api_secret = settings.SMS_API_SECRET

        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = phone_num1  # Recipients Number '01000000000,01000000001'
        params['from'] = phone_num2  # Sender number
        params['text'] = text  # Message

        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            result = 1
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
        # sys.exit()
    context = {
        'result': result
    }
    return render(request, 'sms/send.html', context)
