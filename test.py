import nexussdk as nexus
import json
from decouple import config

# TOKEN has to be set
# in file .env (project root): TOKEN="..."
TOKEN = config('TOKEN')
NEXUS_ENVIRONMENT = config('NEXUS')
ORG = config('ORG')
PROJECT = config('PROJECT')

nexus.config.set_environment(NEXUS_ENVIRONMENT)
nexus.config.set_token(TOKEN)

from kgforge.core import KnowledgeGraphForge
from kgforge.core import Resource
forge = KnowledgeGraphForge("configuration.yml", endpoint=NEXUS_ENVIRONMENT, bucket=ORG + "/" + PROJECT, token=TOKEN, debug=True)


print('types')
forge.types()
print('template')
forge.template('MonetaryGrant')


f = open('test/monetarygrant/monetarygrant.json')
json = json.load(f)

res = forge.from_jsonld(json)

print('grant res', type(res), res)

forge.validate(res)


#forge.register(res, 'http://rescs.org/dash/monetarygrant')
