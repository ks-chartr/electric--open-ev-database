import logging

import requests
import json

from Opendata.settings import SMS_API_AUTHORIZATION_TOKEN


def send_sms_otp(mobile_number):
    # send SMS custom to Open EV
    url = f"https://messages.delhitransport.in/v2/create/{mobile_number}?tid=1107166548167834868"

    payload = {}
    headers = {
        'Authorization': f'Bearer {SMS_API_AUTHORIZATION_TOKEN}'
    }
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def verify_otp(mobile_number, otp):
    url = f"https://messages.delhitransport.in/v2/verify/{mobile_number}/"

    payload = json.dumps({
        "otp": f"{otp}"
    })
    headers = {
        'Authorization': f'Bearer {SMS_API_AUTHORIZATION_TOKEN}',
        'Content-Type': 'application/json'
    }

    print(url)
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


if __name__ == "__main__":
    # send_sms_otp("9818711051")
    # print(verify_otp("1234567890", "3558"))
    pass
