import requests
import json


def get_ip_geo(obs_value):
    url = 'http://ipwhois.app/json/{}'.format(obs_value)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).text
    return json.loads(response)



