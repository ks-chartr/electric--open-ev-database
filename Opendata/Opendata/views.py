from django.shortcuts import render, get_object_or_404, redirect
from contactusform.models import *

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

	return render(request, 'staticData.html', args)

def dynamicData(request):
	args = {}
	return render(request, 'dynamicData.html', args)

def contact(request):
	args = {}
	if (request.method == 'POST'):
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		message = request.POST.get('message')
		contactRequest = ContactRequest (
			email = email,
			phone = phone,
			message = message
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
	args['terms'] = terms
	return render(request, 'terms.html', args)

def privacy(request):
	args = {}
	policy = Policy.objects.all()
	args['policies'] = policy
	return render(request, 'privacy.html', args)
