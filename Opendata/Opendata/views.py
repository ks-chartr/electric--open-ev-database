from django.shortcuts import render, get_object_or_404, redirect
from contactusform.models import ContactRequest

def home(request):
	args = {}
	return render(request, 'index.html', args)

def staticData(request):
	args = {}
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
