from django.shortcuts import render, get_object_or_404, redirect

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
	return render(request, 'contact.html', args)

def about(request):
	args = {}
	return render(request, 'about.html', args)
