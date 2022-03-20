import json

from django.shortcuts import render
from Opendata.decorators import authenticate_api_key
from Opendata.serializers import EVLocationsSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from EVUpdates.models import EVLocations
import io
from rest_framework.renderers import JSONRenderer


# Create your views here.
# TODO: make nested serializers + models
@csrf_exempt
@authenticate_api_key(role='provider')
def addUpdateEV(request, passcode):
    if request.method != 'PUT':
        responseCode = 401
        msg = "Invalid request method"
    else:
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        for ev_data in data:
            ev_data['charger_type'] = json.dumps(ev_data['charger_type'])
            ev_data['contact_numbers'] = json.dumps(ev_data['contact_numbers'])
        responseCode = 200
        serializer = EVLocationsSerializer(EVLocations.objects.all(), data=data, many=True)
        if serializer.is_valid():
            msg = 'valid data'
            serializer.save(provider_passcode=passcode)
            return JsonResponse({"status": responseCode, "msg": msg}, status=responseCode)
        else:
            msg = 'invalid data'
    return JsonResponse({"status": responseCode, "msg": msg}, status=responseCode)


@authenticate_api_key(role='provider')
def deleteEV(request):
    pass


@authenticate_api_key(role='provider')
def getMyEV(request, passcode):
    if request.method != 'GET':
        responseCode = 401
        user_ev_locations_json = {"Invalid request method"}
    else:
        responseCode = 200
        user_ev_locations = EVLocations.objects.filter(provider_passcode=passcode)
        serializer = EVLocationsSerializer(user_ev_locations, many=True)
        user_ev_locations_json = serializer.data
    return JsonResponse({"status": responseCode, "msg": user_ev_locations_json}, status=responseCode)


@authenticate_api_key(role='consumer')
def getEV(request, passcode):
    if request.method != 'GET':
        responseCode = 401
        all_ev_locations_json = {"Invalid request method"}
    else:
        responseCode = 200
        all_ev_locations = EVLocations.objects.all()
        serializer = EVLocationsSerializer(all_ev_locations, many=True)
        all_ev_locations_json = serializer.data
    return JsonResponse({"status": responseCode, "msg": all_ev_locations_json}, status=responseCode)
