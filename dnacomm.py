import requests
import json

import urllib3


class DnaComm:

    def __init__(self):

        self.url = 'https://sandboxdnac.cisco.com/dna'
        self.auth = ('devnetuser', 'Cisco123!')
        self.token = None

    def get_token(self):

        headers = {'Content-Type': 'application/json'}

        auth_resp = requests.post(
            f"{self.url}/system/api/v1/auth/token",
            auth=self.auth, headers=headers,
            verify=False)

        try:
            auth_resp.raise_for_status()
        except requests.HTTPError as e:
            print(str(e))
            return

        self.token = auth_resp.json()['Token']

    def get_device_list(self):

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": self.token
        }

        payload = None

        device_list = requests.get(f"{self.url}/intent/api/v1/network-device",
                                   headers=headers, data=payload)
        try:
            device_list.raise_for_status()
        except requests.HTTPError as e:
            print(str(e))
            return
        return device_list.json()['response']
    
    def add_device(self):

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": self.token
        }

        payload = {
            "ipAddress": ['10.10.20.83'],
            "snmpROCommunity": "readonly",
            "snmpRWCommunity": "readwrite",
            "snmpRetry": "1",
            "snmpTimeout": "60",
            "snmpVersion": "v2",
            "cliTransport": "ssh",
            "userName": "billy",
            "password": "billy123!"
        }

        add_resp = requests.post(f'{self.url}/intent/api/v1/network-device', headers=headers, json=payload)

        try:
            add_resp.raise_for_status()
        except requests.HTTPError as e:
            print(str(e))
            return

        return add_resp


def main():

    urllib3.disable_warnings()
    dna = DnaComm()
    dna.get_token()
    print(dna.token)
    if not dna.token:
        exit(-1)
    devices = dna.get_device_list()
    for device in devices:
        print(f"{device['hostname']}: {device['managementIpAddress']}")


if __name__ == '__main__':
    main()
