#!/usr/bin/env python3

import json
from typing import List
from decouple import config
from pyld import jsonld
from utils.file_helper_methods import absolute_from_rel_file_path
from utils.nexus_interaction import create_schema

# TOKEN has to be set
# in file .env (project root): TOKEN="..."
TOKEN = config('TOKEN')
NEXUS_ENVIRONMENT = config('NEXUS')
ORG = config('ORG')
PROJECT = config('PROJECT')
VERIFY_SSL: bool = bool(int(config('VERIFY_SSL'))) # throws an uncaught error if not numerical / integer

# order in which schemas are created (dependency)
order: List[str] = ['thing', 'person', 'organization', 'place', 'creativework', 'intangible', 'structuredvalue', 'contactpoint',
         'monetaryamount', 'article', 'dataset', 'mediaobject', 'scholarlyarticle', 'datadownload', 'grant',
         'monetarygrant', 'project', 'researchproject']

for schema_name in order:
    print(schema_name)
    f = open(absolute_from_rel_file_path('../shapes/' + schema_name + '/schema.json', __file__))
    schema = json.load(f)
    f.close()

    # expand all prefixes and get rid of remote schema
    creation_res = create_schema(jsonld.compact(schema, {}), NEXUS_ENVIRONMENT, ORG, PROJECT, TOKEN, VERIFY_SSL)
    print(creation_res)

