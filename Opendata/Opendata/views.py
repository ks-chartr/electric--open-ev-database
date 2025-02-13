import mimetypes
import os
import re

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from contactusform.models import *
from django.urls import reverse
from downloadRealDataForm.models import *
from registerDataProvider.models import *
from django.utils.crypto import get_random_string
import hashlib
import logging
from decouple import config
import datetime
from registerDataProvider.admin import authorise as provider_auth
from downloadRealDataForm.admin import authorise as consumer_auth
import urllib.request  # the lib that handles the url stuff

from modules.messaging_service import send_sms_otp, verify_otp

STATIC_DATA_FILE = config('STATIC_DATA_FILE', default='ev_locations.xlsx', cast=str)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert STATIC_DATA_FILE != 'None'

logger = logging.getLogger(__name__)


def auto_authorize(user_email, user_type):
    if user_type == 'provider':
        registered_user = RegisterDataProvider.objects.filter(email=user_email)
        provider_auth("", "", registered_user)
    elif user_type == 'consumer':
        registered_user = DownloadRealData.objects.filter(email=user_email)
        consumer_auth("", "", registered_user)
    else:
        print("invalid auth")


def home(request):
    args = {}
    return render(request, 'index.html', args)


def staticData(request):
    args = {}
    evLastUpdated = EVLastUpdated.objects.all()
    if (len(evLastUpdated)):
        args['evLastUpdated'] = evLastUpdated[0].date

    if request.method == 'POST':
        name = request.POST.get('name') or ''
        email = request.POST.get('email') or ''
        usageType = request.POST.get('usageType')
        purpose = str(request.POST.getlist('purpose'))
        dataDownloaded = request.POST.get('dataDownloaded')

        downloadData = DownloadData(
            name=name,
            email=email,
            usageType=usageType,
            purpose=purpose,
            dataDownloaded=dataDownloaded
        )
        downloadData.save()
        args['success'] = 'success'

        # file_path = os.path.join(BASE_DIR, STATIC_DATA_FILE)
        # file_name_w_extension = os.path.basename(STATIC_DATA_FILE)
        # with open(STATIC_DATA_FILE, "rb") as excel:
        #     data = excel.read()
        # response = HttpResponse(data,
        #                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name_w_extension)
        # response['X-Accel-Redirect'] = "/protected/{0}".format(file_name_w_extension)

        # return response
        return HttpResponseRedirect("https://ev.delhi.gov.in/openev/static/assets/ev_locations.xlsx")

    return render(request, 'staticData.html', args)


def realtimeData(request):
    args = {}
    if request.method == 'POST':
        name = request.POST.get('name') or ''
        email = request.POST.get('email') or ''
        number = request.POST.get('countryCode') + request.POST.get('number') or ''
        companyName = request.POST.get('companyName') or ''
        purpose = str(request.POST.getlist('purpose')) or ''
        description = request.POST.get('description') or ''
        usageType = request.POST.get('usageType')
        if request.POST.get('subscribed'):
            subscribed = True
        else:
            subscribed = False
        downloadRealData = DownloadRealData(
            name=name,
            email=email,
            number=number,
            companyName=companyName,
            purpose=purpose,
            usageType=usageType,
            description=description,
            subscribed=subscribed
        )
        try:
            downloadRealData.save()
            args['email'] = email
            args['number'] = number
            args['success'] = 'success'
            unique_id = get_random_string(length=32)
            args['unique_id'] = unique_id
            downloadRealData.passCode = hashlib.sha224(unique_id.encode('utf-8')).hexdigest()
            downloadRealData.save()
            auto_authorize(user_email=email, user_type="consumer")
        except Exception as e:
            args['e'] = str(e).split(":")[0] == 'UNIQUE constraint failed'
            args['email'] = email
            args['number'] = number
            print(e)
    return render(request, 'realtimeData.html', args)


def dataProvider(request):
    args = {}
    if request.method == 'POST':
        name = request.POST.get('name') or ''
        email = request.POST.get('email') or ''
        number = request.POST.get('countryCode') + request.POST.get('number') or ''
        companyName = request.POST.get('companyName') or ''
        # purpose = str(request.POST.getlist('purpose')) or ''
        description = request.POST.get('description') or ''
        # usageType = request.POST.get('usageType')
        authorisation_letter = request.FILES.get('authorisationLetter')
        company_website = request.POST.get('companyWebsite')
        operational_since = request.POST.get('operationalSince')

        if authorisation_letter:
            authorisation_letter.name = f"{companyName}_{name}_{authorisation_letter.name}"

        if request.POST.get('swapping'):
            battery_swapping = True
        else:
            battery_swapping = False

        if request.POST.get('charging'):
            charging = True
        else:
            charging = False

        if request.POST.get('dtl'):
            dtl = True
        else:
            dtl = False
        if request.POST.get('nondtl'):
            nondtl = True
        else:
            nondtl = False

        registerDataProvider = RegisterDataProvider(
            name=name,
            email=email,
            number=number,
            companyName=companyName,
            description=description,
            dtl_sites=dtl,
            nondtl_sites=nondtl,
            authorisation_letter=authorisation_letter,
            company_website=company_website,
            operational_since=operational_since,
            battery_swapping=battery_swapping,
            charging=charging
        )
        try:
            valid_file_formats = ["doc", "docx", "pdf"]
            if not any(file_format in authorisation_letter.name for file_format in valid_file_formats):
                args['invalid_file'] = True
            else:
                # verify OTP, if 200 proceed else return
                registerDataProvider.save()
                # request.session["mobile_number"] = number
                return redirect(f'/openev/verify/otp?pk={registerDataProvider.pk}')
        except Exception as e:
            args['e'] = True if str(e).lower().__contains__('unique constraint') else False
            args['email'] = email
            args['number'] = number
            print(e)

    return render(request, 'dataProvider.html', args)


'''
	response codes
	
	400: invalid request
	403: unauthorised token
'''


def authenticate_api_key(request):
    responseCode = 401
    passCode = None
    msg = ''
    if request.method != 'GET':
        responseCode = 401
    else:
        # GET REQUEST

        # fetch key from original request url
        passCode = request.GET.get('key')
        if passCode is None:
            print('no key found in URL')
            try:
                passCode = request.META.get('HTTP_X_ORIGINAL_URI').split('key=')[-1]
                print('key found in HTTP_X_ORIGINAL_URI: {}'.format(passCode))
            except Exception as err:
                print(err)
                print('no key found in HTTP_X_ORIGINAL_URI')

        if passCode is None or passCode.isalnum() == False:
            responseCode = 401
            msg = 'Invalid key.'
        elif passCode.isalnum():
            try:
                # print("old: {}".format(passCode))
                passCode = hashlib.sha224(passCode.encode('utf-8')).hexdigest()
                # print("new: {}".format(passCode))
                downloadRealData = DownloadRealData.objects.get(passCode=passCode)
                if downloadRealData is None:
                    responseCode = 401
                    msg = 'Invalid key.'
                elif not downloadRealData.authorised:
                    responseCode = 401
                    msg = 'Key not authorised.'
                else:
                    # ONLYVALIDCASE
                    msg = 200
                    responseCode = 200
                    downloadRealData.hitsAllTime += 1
                    downloadRealData.lastHit = datetime.datetime.now()
                    downloadRealData.save()

            except Exception as e:
                logging.info(e)
                responseCode = 401
                msg = 'Unknown error.'
        else:
            responseCode = 401

    response = JsonResponse({'status': responseCode, 'msg': msg}, status=responseCode)
    return response


def contact(request):
    args = {}
    if (request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        contactRequest = ContactRequest(
            name=name,
            email=email,
            message=message,
            subject=subject
        )
        contactRequest.save()
        args['success'] = 'succcess'
    return render(request, 'contact.html', args)


def about(request):
    args = {}
    return render(request, 'about.html', args)


def documentation(request):
    args = {}
    return render(request, 'documentation.html', args)


def terms(request):
    args = {}
    terms = Terms.objects.all()
    # print(terms)
    if (terms):
        args['terms'] = terms
        return render(request, 'terms.html', args)
    return HttpResponseRedirect("/static/assets/terms-and-conditions.pdf")


def policy(request):
    args = {}
    # policy = Policy.objects.all()
    # args['policies'] = policy
    return HttpResponseRedirect("/static/assets/policy.pdf")


# return render(request, 'privacy.html', args)


def privacy(request):
    args = {}
    # policy = Policy.objects.all()
    # args['policies'] = policy
    return HttpResponseRedirect("/static/assets/privacy.pdf")


# return render(request, 'privacy.html', args)


def announcement(request):
    args = {}
    announcements = Announcement.objects.all().order_by('-createdAt')[::-1]
    if (announcements):
        args['announcements'] = announcements
    return render(request, 'announcement.html', args)


def send_otp(request, mobile_number_str):
    return send_sms_otp(mobile_number_str)


PHONE_NUM_PATTERN = re.compile("^[5-9]\d{9}$")
from django.contrib import messages


def verify_mobile_number(request):
    """
    :param request: user's mobile number in payload
    :return: render verify mobile number page
    """

    try:
        mobile_number = request.session["mobile_number"]
    except Exception as e:
        pass

    send_sms_otp(mobile_number)
    # TODO: redirect to OTP input screen
    return redirect(f'/openev/verify/otp')  # ?mobile_number={mobile_number_str}')

    """
    if request.method == 'GET':
        # last_two_digits = mobile_number_str[-2:]
        # response = send_sms_otp(mobile_number_str)
        # args = {"mobile_number_text": f"xxxxxxxx{last_two_digits}", "message": f"{response['description']}",
        #         "registerDataProviderObj": registerDataProviderObj}
        return render(request, 'mobileVerify.html')
    elif request.method == 'POST':
        # TODO: send OTP
        # TODO: redirect to OTP input screen
        mobile_number_str = request.POST.get('mobile_number')
        if not PHONE_NUM_PATTERN.match(mobile_number_str):
            messages.error(request, 'Invalid mobile number.')
            return HttpResponseRedirect(request.path_info)

        # send sms
        # TODO: uncomment for production
        send_sms_otp(mobile_number_str)
        # TODO: redirect to OTP input screen
        return redirect(f'/openev/verify/otp')  # ?mobile_number={mobile_number_str}')
    """


def verify_otp_view(request):
    """
    :param pk:
    :param request: user's mobile number in payload
    :return: render verify mobile number page
    """
    try:
        # mobile_number = request.session["mobile_number"]
        # assert mobile_number is not None

        pk = int(request.GET.get('pk'))
        obj = RegisterDataProvider.objects.get(pk=pk)
        # assert obj is not None
        # if not PHONE_NUM_PATTERN.match(mobile_number):
        #     messages.error(request, 'Invalid mobile number.')
        #     return HttpResponseRedirect(request.path_info)
    except Exception as e:
        # del request.session['mobile_number']
        messages.error(request, 'Invalid user.')
        return render(request, 'otpVerify.html')

    mobile_number = obj.number[-10:]
    if request.method == 'GET':
        # send OTP sms
        send_sms_otp(mobile_number)
        return render(request, 'otpVerify.html',
                      context={"mobile_number": mobile_number,
                               "mobile_number_text": f"xxxxxxxx{mobile_number[-2:]}"})

    elif request.method == 'POST':
        otp = request.POST.get('otp')
        if len(otp) != 4:
            messages.error(request, 'Invalid OTP.')
            return HttpResponseRedirect(request.path_info)

        # send sms
        response = verify_otp(mobile_number, otp)
        if response.status_code in range(200, 300):
            # TODO: create api key and save it

            args = {'email': obj.email, 'number': mobile_number, 'success': 'success'}
            unique_id = get_random_string(length=32)
            args['unique_id'] = unique_id
            obj.passCode = hashlib.sha224(unique_id.encode('utf-8')).hexdigest()
            obj.save()

            messages.success(request, f'API KEY: {unique_id}')
            # TODO: redirect to OTP input screen

            return redirect("/openev/data/provider/")
        else:
            messages.error(request, f'{response.json()["description"]}')
            return HttpResponseRedirect(request.path_info)
