import requests
import json
import time


def get_bearer_token(root_url_api, username, password, client_secret):
    requests.packages.urllib3.disable_warnings()
    url=f'{root_url_api}:3334/connect/token'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "username": username,
        "password": password,
        "client_id": "mpx",
        "client_secret": client_secret,
        "grant_type": "password",
        "response_type": "code id_token token",
        "scope": "offline_access mpx.api ptkb.api"
    }

    response = requests.request(method='POST', url=url, headers=headers, data=data, verify=False)
    token = json.loads(response.text)["access_token"]

    return token


def get_events_by_filter(root_url_api, access_token, filter, time_from, time_to=None):
    requests.packages.urllib3.disable_warnings()
    url = f'{root_url_api}/api/events/v2/events?limit=10000'

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    data = {
      "filter": filter,
      "groupValues": [],
      "timeFrom": time_from,
      "timeTo": time_to
    }

    response = requests.request(method='POST', url=url, headers=headers, data=json.dumps(data), verify=False)
    events = json.loads(response.text)["events"]
    total_count = json.loads(response.text)["totalCount"]
    last_incident_time = events[-1]["time"]

    return events, total_count, last_incident_time


def get_country_by_ip(ip_address):
    try:
        url = f"https://api.iplocation.net/?ip={ip_address}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            country = data.get('country_name')
            return country
        else:
            return f"Ошибка: API error {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
