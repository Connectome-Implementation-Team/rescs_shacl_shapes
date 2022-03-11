#!/usr/bin/env python3

import json
import sys
from typing import List, Optional, Dict
from decouple import config
from utils.file_helper_methods import absolute_from_rel_file_path
from utils.nexus_interaction import get_composite_view, update_composite_view, create_composite_view

# TOKEN has to be set
# in file .env (project root): TOKEN="..."
TOKEN = config('TOKEN')
NEXUS_ENVIRONMENT = config('NEXUS')
ORG = config('ORG')
PROJECT = config('PROJECT')
VERIFY_SSL: bool = bool(int(config('VERIFY_SSL')))  # throws an uncaught error if not numerical / integer

def get_args() -> List[str]:
    argv = sys.argv[1:]

    if len(argv) < 1:
        print('Usage: ' + sys.argv[0] + ' <composite_view_name> (<composite_view_name> without file extension)')
        print('Example: ' + sys.argv[0] + ' dataset (see files in directory "compositeviews")')
        exit(1)
    else:
        return argv


# get args
args = get_args()

for view_name in args:

    # get composite view
    f = open(absolute_from_rel_file_path('../compositeviews/' + view_name + '/composite_view.json', __file__), 'r')
    comp_view = json.load(f)
    f.close()

    # get sparql projection belonging to composite view
    f = open(absolute_from_rel_file_path('../compositeviews/' + view_name + '/es_projection_query.rq', __file__), 'r')
    sparql_proj_query = f.read()
    f.close()

    # add sparql projection to composite view
    comp_view['projections'][0]['query'] = sparql_proj_query

    comp_view_rev: Optional[Dict] = get_composite_view(comp_view['@id'], NEXUS_ENVIRONMENT, ORG, PROJECT, TOKEN, VERIFY_SSL)

    if comp_view_rev is not None:
        # composite view already exists, update it in Nexus
        try:
            rev = int(comp_view_rev['_rev'])
        except KeyError as e:
            raise Exception('No _rev given in composite view')

        update_res = update_composite_view(comp_view, rev, NEXUS_ENVIRONMENT, ORG, PROJECT, TOKEN, VERIFY_SSL)
        print('updated:', update_res)
    else:
        # composite view does not exist yet in Nexus, create it
        created_res = create_composite_view(comp_view, NEXUS_ENVIRONMENT, ORG, PROJECT, TOKEN, VERIFY_SSL)
        print('created:', created_res)
