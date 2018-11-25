import os

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from contactusform.models import *
from downloadRealDataForm.models import *
from django.utils.crypto import get_random_string
import hashlib
import logging
from decouple import config

STATIC_DATA_FILES_URL = config('STATIC_DATA_FILES_URL', default='http://192.168.2.231:8000/', cast=str)
assert STATIC_DATA_FILES_URL != 'None'

logger = logging.getLogger(__name__)

def home(request):
	args = {}
	return render(request, 'index.html', args)


def staticData(request):
	args = {}
	routesLastUpdated = RoutesLastUpdated.objects.all()
	if (len(routesLastUpdated)):
		args['routesLastUpdated'] = routesLastUpdated[0].date

	stopTimeLastUpdated = StopTimeLastUpdated.objects.all()
	if (len(stopTimeLastUpdated)):
		args['stopTimeLastUpdated'] = stopTimeLastUpdated[0].date

	tripsLastUpdated = TripsLastUpdated.objects.all()
	if (len(tripsLastUpdated)):
		args['tripsLastUpdated'] = tripsLastUpdated[0].date

	stopLastUpdated = StopLastUpdated.objects.all()
	if (len(stopLastUpdated)):
		args['stopLastUpdated'] = stopLastUpdated[0].date

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

		import urllib.request  # the lib that handles the url stuff
		URL = '{}/{}.txt'.format(STATIC_DATA_FILES_URL, dataDownloaded)
		print(URL)
		test_file = urllib.request.urlopen(URL)
		# test_file = open('/Users/atul/Desktop/tmp/{}.txt'.format(dataDownloaded), 'rb')
		response = HttpResponse(content=test_file)
		response['Content-Type'] = 'text/plain'
		response['Content-Disposition'] = 'attachment; filename="%s.txt"' % dataDownloaded
		return response
		# response = JsonResponse({'status': 200,}, status=responseCode)
		# return response

		# return HttpResponseRedirect('http://traffickarma.iiitd.edu.in:9010/static/' + dataDownloaded + '.txt')

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
		except Exception as e:
			args['e'] = str(e).split(":")[0] == 'UNIQUE constraint failed'
			args['email'] = email
			args['number'] = number
			print(e)
	# else:
	# passCode = request.GET.get('key')
	# if passCode:
	# 	print('passCode', passCode)
	# 	try:
	# 		downloadRealData = DownloadRealData.objects.get(passCode=passCode)
	# 		if downloadRealData.authorised:
	# 			return HttpResponseRedirect('http://traffickarma.iiitd.edu.in:9010/static/stops.txt')
	# 		else:
	# 			args['notAuthorised'] = '"' + str(passCode) + '" is not authorise yet!'
	# 	except:
	# 		args['notAuthorised'] = '"' + str(passCode) + '" is an invalid Key '
	return render(request, 'realtimeData.html', args)

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
			except Exception:
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
