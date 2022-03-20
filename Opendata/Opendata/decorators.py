from django.http import JsonResponse
from downloadRealDataForm.models import *
from registerDataProvider.models import *
import hashlib
from functools import wraps
from datetime import datetime


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def authenticate_api_key(view_function, role):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        responseCode = 401
        passCode = None
        msg = ''
        request = args[0]
        if request.method not in ['GET', 'PUT', 'DELETE']:
            responseCode = 401
            msg = 'Invalid request method'
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
                    if role == 'provider':
                        user_obj = RegisterDataProvider.objects.get(passCode=passCode)
                    elif role == 'consumer':
                        user_obj = DownloadRealData.objects.get(passCode=passCode)
                    else:
                        user_obj = None
                    if user_obj is None:
                        responseCode = 401
                        msg = 'Invalid key.'
                    elif not user_obj.authorised:
                        responseCode = 401
                        msg = 'Key not authorised.'
                    else:
                        # ONLYVALIDCASE
                        msg = 200
                        responseCode = 200
                        user_obj.hitsAllTime += 1
                        user_obj.lastHit = datetime.now()
                        user_obj.save()
                        return view_function(*args, **kwargs, passcode=passCode)
                except RegisterDataProvider.DoesNotExist:
                    responseCode = 401
                    msg = 'Invalid key.'
                except DownloadRealData.DoesNotExist:
                    responseCode = 401
                    msg = 'Invalid key.'
                except Exception as e:
                    responseCode = 401
                    msg = 'Unknown error.'
            else:
                responseCode = 401
            response = JsonResponse({'status': responseCode, 'msg': msg}, status=responseCode)
            return response
    return decorated_function
