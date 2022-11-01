import json

import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required

from Opendata.decorators import authenticate_api_key
from Opendata.serializers import EVLocationsSerializer, ConnectorMappingSerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from EVUpdates.models import EVLocations, ConnectorMapping
import io


def make_json(evlocations_response):
    for evlocation in evlocations_response:
        evlocation["charger_type"] = json.loads(evlocation["charger_type"].replace("'", '"'))
        evlocation["coordinates"] = json.loads(evlocation["coordinates"].replace("'", '"'))
        evlocation["contact_numbers"] = json.loads(evlocation["contact_numbers"].replace("'", '"'))


# Create your views here.
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


@staff_member_required
def openEVDashboard(request):
    args = {}
    if request.method != 'GET':
        responseCode = 401
        all_ev_locations_json = {"Invalid request method"}
        return JsonResponse({"status": responseCode, "msg": all_ev_locations_json}, status=responseCode)
    else:
        responseCode = 200

        all_connector_mapping = ConnectorMapping.objects.all()
        serializer = ConnectorMappingSerializer(all_connector_mapping, many=True)
        connector_mapping = serializer.data
        connector_mapping_dict = {connector_map["vendor_connector_name"]: connector_map["mapped_connector_name"] for
                                  connector_map in connector_mapping}

        all_ev_locations = EVLocations.objects.all()
        serializer = EVLocationsSerializer(all_ev_locations, many=True)
        all_ev_locations_json = serializer.data
        make_json(all_ev_locations_json)
        df = pd.DataFrame.from_records(all_ev_locations_json)
        res_list = list()
        for vendor, vendor_group in df.groupby("vendor"):
            all_locations_charger_types = vendor_group.charger_type.values
            vendor_data_dict = dict()
            vendor_data_dict["Name of the player"] = vendor
            vendor_data_dict["Data provided type"] = "API"
            n_battery_stations = vendor_group.station_type.value_counts().get('battery_swapping')
            n_charging_stations = vendor_group.station_type.value_counts().get('charging')
            vendor_data_dict["Total Battery Swapping Stations added"] = 0 if n_battery_stations is None else int(
                n_battery_stations)
            vendor_data_dict["Total Charging points added"] = 0 if n_charging_stations is None else int(
                n_charging_stations)
            for location_charger_type in all_locations_charger_types:
                for charger_type in location_charger_type:
                    mapped_connector_name = connector_mapping_dict.get(charger_type["type"])
                    connector_name = mapped_connector_name if mapped_connector_name is not None else charger_type["type"]
                    if vendor_data_dict.get(connector_name) is None:
                        vendor_data_dict[connector_name] = int(float(charger_type["total"]))
                    else:
                        vendor_data_dict[connector_name] += int(float(charger_type["total"]))
            res_list.append(vendor_data_dict)
        res_df = pd.DataFrame.from_records(res_list)
        res_df = res_df.fillna(0)
        args["tables"] = res_df.to_html(index=False)
        return render(request, 'dashboard.html', args)
