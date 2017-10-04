import requests
import json

response = requests.post(
    'http://localhost:8000/api/v2/datalogger/dsmrreading',
    headers={'X-AUTHKEY': '2F31RWYH2LXPMQ2QXNV50HV2I1NBCVJU6PNDAUG7M47R4HO93N7P4TC8T5Q6FU7J'},
    data={
        'electricity_currently_delivered': 1.500,
        'electricity_currently_returned': 0.025,
        'electricity_delivered_1': 2000,
        'electricity_delivered_2': 3000,
        'electricity_returned_1': 0,
        'electricity_returned_2': 0,
        'timestamp': '2017-09-26T00:00:00+02',
    }
)

if response.status_code != 201:
    print('Error: {}'.format(response.text))
else:
    print('Created: {}'.format(json.loads(response.text)))
