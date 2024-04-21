#!/usr/bin/env python3

'''
    This script uses environment varables for server ID and password
    so it shouldn't be left around either in command histroy or in
    your envronment. Because of this, it's best to clean up your shell
    on Mac/Linux like so:

    ```
        export FNO_SERVER=ABCD12345678
        read -s FNO_PASSWORD && export FNO_PASSWORD
        chmod +x ./license-counts.py
        ./license-counts.py
        unset FNO_PASSWORD
    ```

    On Windows, make sure to use Command Prompt instead of PowerShell and
    do this:
    ```
        set FNO_SERVER=ABCD12345678
        set FNO_PASSWORD=some+great+password!
        python3 license-counts.py
        set FNO_PASSWORD=
    ```
'''

import os
import requests
import time
from prometheus_client import Gauge, start_http_server

SITE_ID = 'teradici.compliance.flexnetoperations.com'
SERVER_ID = os.environ['FNO_SERVER']
SERVER_BASE_URL = 'https://{0}/api/1.0/instances/{1}'.format(SITE_ID, SERVER_ID)
SERVER_LOGIN_URL = SERVER_BASE_URL + '/authorize'
SERVER_FEATURE_SUMMARY_URL = SERVER_BASE_URL + '/features/summaries'
SERVER_CLIENT_SUMMARY_URL = SERVER_BASE_URL + '/clients'

login_dict = {
    'user': 'admin',
    'password': os.environ['FNO_PASSWORD']
}

g = Gauge('pcoip', 'pcoip license usage as reported by teradici',['feature','entitlement'])
client_gauge = Gauge('pcoip_client', 'Presence of PCoIP active session', ['hostname'])
PORT = int(os.getenv("LISTEN_PORT",9777))
print("starting server on port {}".format(PORT))
start_http_server(PORT)

while True:
    session = requests.Session()

    try:
        login_request = session.post(SERVER_LOGIN_URL, json = login_dict).json()
    except Exception as e:
        print("Error when trying to log in: {}".format(str(e)))

    auth_token = login_request['token']

    auth_header = {
        'Authorization': 'Bearer {}'.format(auth_token)
    }

    try:
        data = session.get(url=SERVER_FEATURE_SUMMARY_URL, headers=auth_header).json()
        clientData = session.get(url=SERVER_CLIENT_SUMMARY_URL, headers=auth_header).json()
        client_gauge.clear()
        g.clear()
    except Exception as e:
        print("Error while collecting capabilities: {}".format(e))

    clients = []
    total_count_sum = 0
    total_used_sum = 0
    for key, value in data.items():
        print(key)
        if key == "Agent-Graphics":
                for date, data in value.items():
                    total_count_sum += data['totalCount']
                    total_used_sum += data['totalUsed']
    for entry in clientData:
        for key, value in entry.items():
            if key == "hostName":
                clients.append(value)
                client_gauge.labels(hostname=value).set(1)
            
    g.labels("pcoip_licenses","used").set(total_used_sum)
    g.labels("pcoip_licenses","entitled").set(total_count_sum)

    time.sleep(30)