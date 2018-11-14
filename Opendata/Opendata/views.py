from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from contactusform.models import *
from downloadRealDataForm.models import *
from django.utils.crypto import get_random_string

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
		return HttpResponseRedirect('http://traffickarma.iiitd.edu.in:9010/static/'+dataDownloaded+'.txt')

	return render(request, 'staticData.html', args)


def dynamicData(request):
	args = {}
	if request.method == 'POST':
		name = request.POST.get('name') or ''
		email = request.POST.get('email') or ''
		number = request.POST.get('number') or ''
		companyName = request.POST.get('companyName') or ''
		purpose = str(request.POST.getlist('purpose')) or ''
		description = request.POST.get('description') or ''
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
			description=description,
			subscribed=subscribed
		)
		try:
			downloadRealData.save()
			args['email'] = email
			args['number'] = number
			args['success'] = 'success'
			unique_id = get_random_string(length=32)
			downloadRealData.passCode = unique_id
			downloadRealData.save()
		except Exception as e:
			args['e'] = str(e).split(":")[0] == 'UNIQUE constraint failed'
			args['email'] = email
			args['number'] = number
			print(e)
	else:
		passCode = request.GET.get('passCode')
		if passCode:
			print('passCode', passCode)
			downloadRealData = get_object_or_404(DownloadRealData, passCode=passCode)
			print(downloadRealData)
			if downloadRealData.authorised:
				return HttpResponseRedirect('http://traffickarma.iiitd.edu.in:9010/static/stops.txt')
			else:
				args['notAuthorised'] = 'notAuthorised'


	return render(request, 'dynamicData.html', args)


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
