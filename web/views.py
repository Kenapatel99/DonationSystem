import base64
import os
import math
import random
import smtplib

import pyotp
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
from website.settings import *
from . import Checksum
from .models import Member, PaytmHistory, Payment
import pandas as pd
from datetime import datetime


# class BaseAuthValidSourceAndToken(viewsets.ReadOnlyModelViewSet):
#     authentication_classes = []
#     permission_classes = [IsValidSourceAndToken]

# # This class returns the string needed to generate the key
# class generateKey:
#     @staticmethod
#     def returnValue(phone):
#         return str(phone) + str(datetime.date(datetime.now())) + "1234"


# Create your views here.

def index(request):
    print(request)
    if request.method == 'POST':
        if Member.objects.filter(username=request.POST['username']).exists():
            context = {'msg': 'User name already exist'}
            return render(request, 'web/index.html', context)
        else:
            print(request)
            member = Member(username=request.POST['username'], password=request.POST['password'],
                            firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                            contactNo=request.POST['contactNo'])
            member.save()
            return render(request, 'web/login.html')
    else:
        return render(request, 'web/index.html')


def login(request):
    print("request", request)
    return render(request, 'web/login.html')


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if Member.objects.filter(username=username, password=password).exists():

            # get member contact details
            member_data = pd.DataFrame(Member.objects.filter(username=username).values())
            contactNo = member_data['contactNo'][0]
            contactNo = int(contactNo)

            # Generate otp and send in registered number.
            generate_key = generateOTP()
            otp = int(generate_key)

            # for Encrypted OTP Generation---->>>
            # contactNo.counter += 1  # Update Counter At every Call
            # keygen = generateKey()
            # key = base64.b32encode(keygen.returnValue(contactNo).encode())  # Key is generated
            # OTP = pyotp.TOTP(key, interval=1000)  # TOTP Model for OTP is created

            # save otp
            Member.objects.filter(contactNo=contactNo, username=username).update(otp=otp)
            member_data_dict = member_data.to_dict(orient="records")
            print("OTP:-->", otp)
            # return render(request, 'web/home.html', {'member': member})
            context = {'OTP': otp, 'contactNo': contactNo}
            return render(request, 'web/verification.html', context)

        else:
            context = {'msg': 'Invalid username or password'}
            return render(request, 'web/login.html', context)


@api_view(['POST'])
def otp_verification(request):
    request_data = request.data
    ContactNo = request_data.get('ContactNo')
    otp = request_data.get('otp')
    # verify weather otp matches registered no or not.
    # get member contact details
    member_data = pd.DataFrame(Member.objects.filter(contactNo=ContactNo).values())
    reg_otp = member_data['otp'][0]
    print("::reg OTP::", reg_otp)

    if otp == reg_otp:
        context = {'msg': 'Otp verified Successfully', 'contactNo': ContactNo}
        # print("Otp verified Successfully")
        return render(request, 'web/member.html', context)
    else:
        context = {
            'msg': 'You are not authorised'
        }
        return render(request, 'web/verification.html', context)

@api_view(['POST'])
def member(request):

    request_data = request.data
    ContactNo = request_data.get('ContactNo')
    donation_amount = request_data.get('amount')

    # get user detail from contact no
    member_data = pd.DataFrame(Member.objects.filter(contactNo=ContactNo).values())
    member_id = member_data['member_id'][0]

    # Update Payment in payment table.
    Payment.objects.create(member_id = member_id,payment = donation_amount)
    return render(request, 'web/payment.html')


def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""
    # length of password can be changed by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

# Api's for payment


# def home1(request):
#     return HttpResponse("<html><a href='"+ settings.HOST_URL +"/paytm/payment'>PayNow</html>")


def payment(request):
    MERCHANT_KEY = PAYTM_MERCHANT_KEY
    MERCHANT_ID = PAYTM_MERCHANT_ID
    print("MERCHANT_ID",MERCHANT_ID)
    print("MERCHANT_KEY",MERCHANT_KEY)
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = HOST_URL + get_lang + PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()

    bill_amount = 100
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':str(order_id),
                    'TXN_AMOUNT': str(bill_amount),
                    'CUST_ID':'demo@google.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    # 'CALLBACK_URL': 'http://localhost:8000/response'
                    #'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        param_dict['CHECKSUMHASH'] = 'gFvROKdAeDuHDmOAcZOMzQl1RB6fJ4QmjS0/WD+T6X/jdZVCsjfv9VmTnhbHBJbjSMGxcwHucMR45QAYhFYhdQVhOJ1orY5qK5+sx6sul4o='
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(param_dict['CHECKSUMHASH'])
        return render(request,"web/payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    print("inside paytm response:",request)
    if request.method == "POST":
        MERCHANT_KEY = PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            PaytmHistory.objects.create(member=request.user, **data_dict)
            return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)