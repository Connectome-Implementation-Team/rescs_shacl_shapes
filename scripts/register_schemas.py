#!/usr/bin/env python3

import os
import json
import requests
from decouple import config
from typing import List
from typing import Dict

# TOKEN has to be set
# in file .env (project root): TOKEN="..."
TOKEN = config('TOKEN')
NEXUS_ENVIRONMENT = config('NEXUS')
ORG = config('ORG')
PROJECT = config('PROJECT')

def absolute_from_rel_file_path(relative_path: str) -> str:
    """
    Given a path relative to this file,
    returns the absolute path.

    :param relative_path: The path relative to this file.
    :return: The absolute path.
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, relative_path)

def create_schema(schema: Dict)-> None:
    """
    Given a schema, registers it in Nexus.

    :param schema: The schema to be created.
    """
    req = requests.post(
        NEXUS_ENVIRONMENT + '/schemas/' + ORG + '/' + PROJECT,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TOKEN}'
        }, data=json.dumps(schema))

    print(req.status_code)
    print(req.json())

# order in which schemas are created (dependency)
order: List[str] = ['thing', 'person', 'organization', 'place', 'creativework', 'intangible', 'structuredvalue', 'contactpoint',
         'monetaryamount', 'article', 'dataset', 'mediaobject', 'scholarlyarticle', 'datadownload', 'grant',
         'monetarygrant', 'project', 'researchproject']

for schema_name in order:
    print(schema_name)
    f = open(absolute_from_rel_file_path('../shapes/' + schema_name + '/schema.json'))
    schema = json.load(f)
    f.close()

    # remove remote context
    orig_context = schema['@context']
    schema['@context'] = orig_context[1]

    create_schema(schema)


