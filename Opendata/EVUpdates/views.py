import json

from Opendata.decorators import authenticate_api_key
from Opendata.serializers import EVLocationsSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from EVUpdates.models import EVLocations
import io


def make_json(evlocations_response):
    for evlocation in evlocations_response:
        evlocation["charger_type"] = json.loads(evlocation["charger_type"].replace("'", '"'))
        evlocation["coordinates"] = json.loads(evlocation["coordinates"].replace("'", '"'))
        evlocation["contact_numbers"] = json.loads(evlocation["contact_numbers"].replace("'", '"'))


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
            #     ev_data['charger_type'] = json.dumps(ev_data['charger_type'])
            ev_data['contact_numbers'] = json.dumps(ev_data['contact_numbers'])
        responseCode = 200
        serializer = EVLocationsSerializer(EVLocations.objects.all(), data=data, many=True)
        if serializer.is_valid():
            msg = 'data updated successfully!'
            serializer.save(provider_passcode=passcode)
            return JsonResponse({"status": responseCode, "msg": msg}, status=responseCode)
        else:
            msg = f'{serializer.errors}'
    return JsonResponse({"status": responseCode, "msg": msg}, status=responseCode)


@authenticate_api_key(role='provider')
def deleteEV(request, passcode):
    if request.method != 'GET':
        responseCode = 401
        msg = "Invalid request method"
    else:
        id = request.GET.get('id')
        responseCode = 200
        EVLocations.objects.filter(provider_passcode=passcode, id=id).delete()
        msg = f"Successfully deleted station for station ID - {id}"
    return JsonResponse({"status": responseCode, "msg": msg}, status=responseCode)


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
        make_json(user_ev_locations_json)
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
        make_json(all_ev_locations_json)
    return JsonResponse({"status": responseCode, "msg": all_ev_locations_json}, status=responseCode)
