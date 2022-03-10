#!/usr/bin/env python3

from decouple import config
import requests
import json
from typing import Dict
from typing import List
from urllib import parse
import sys

from utils.file_helper_methods import absolute_from_rel_file_path
from utils.nexus_interaction import get_composite_view

# TOKEN has to be set
# in file .env (project root): TOKEN="..."
TOKEN = config('TOKEN')
NEXUS_ENVIRONMENT = config('NEXUS')
ORG = config('ORG')
PROJECT = config('PROJECT')
VERIFY_SSL: bool = bool(int(config('VERIFY_SSL'))) # throws an uncaught error if not numerical / integer

def update_composite_view(composite_view: Dict) -> None:
    """
    Given a CompositeView, updates it in Nexus.
    """

    # get composite view's id
    composite_view_id = composite_view['@id']

    # get the current revision of the composite view
    composite_view_rev = get_composite_view(composite_view_id, NEXUS_ENVIRONMENT, ORG, PROJECT, TOKEN, VERIFY_SSL)

    if composite_view_rev is None:
        # composite view does not exist yet
        return None

    # store the current revision number
    rev: int = int(composite_view_rev['_rev'])

    req = requests.put(
        NEXUS_ENVIRONMENT + '/views/' + ORG + '/' + PROJECT + '/' + parse.quote_plus(NEXUS_ENVIRONMENT + '/resources/' + ORG + '/' + PROJECT + '/_/' + composite_view_id),
        params={ 'rev': rev },
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}'
        },
        data=json.dumps(composite_view),
        verify=VERIFY_SSL
    )

    print(req.status_code)
    print(req.json())


def get_args() -> List[str]:
    argv = sys.argv[1:]

    if len(argv) != 1:
        print('Usage: ' + sys.argv[0] + ' <composite_view_name>')
        print('Example: ' + sys.argv[0] + ' dataset')
        exit(1)
    else:
        return argv

# get args
args = get_args()

for view_name in args:
    f = open(absolute_from_rel_file_path('../compositeviews/' + view_name + '.json', __file__))
    view = json.load(f)
    f.close()

    update_composite_view(view)
