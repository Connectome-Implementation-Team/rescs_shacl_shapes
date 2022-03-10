#!/usr/bin/env python3

from decouple import config
import requests
import json
from typing import Dict
from typing import List

from utils.file_helper_methods import absolute_from_rel_file_path

# TOKEN has to be set
# in file .env (project root): TOKEN="..."
TOKEN = config('TOKEN')
NEXUS_ENVIRONMENT = config('NEXUS')
ORG = config('ORG')
PROJECT = config('PROJECT')
VERIFY_SSL: bool = bool(int(config('VERIFY_SSL'))) # throws an uncaught error if not numerical / integer

def create_composite_view(composite_view: Dict) -> None:
    """
    Given a CompositeView, registers it in Nexus.
    """

    req = requests.post(
        NEXUS_ENVIRONMENT + '/views/' + ORG + '/' + PROJECT,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}'
        }, data=json.dumps(composite_view), verify=VERIFY_SSL)

    print(req.status_code)
    print(req.json())


order: List[str] = ['dataset']

for view_name in order:
    f = open(absolute_from_rel_file_path('../compositeviews/' + view_name + '.json', __file__))
    view = json.load(f)
    f.close()

    create_composite_view(view)
