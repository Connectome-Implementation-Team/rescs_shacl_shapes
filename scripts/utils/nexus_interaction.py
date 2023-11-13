#
#      RESCS SHACL Shapes: Build Tools for the RESCS SHACL Shapes Library
#      Copyright (C) 2022 SWITCH
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as published
#      by the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from typing import Dict, Union
from urllib import parse
import json

def create_schema(schema: Dict, nexus_url: str, organisation: str, project: str, token: str, verify_ssl=True) -> Dict:
    """
    Given a schema, registers it in Nexus.

    :param schema: The schema to be created.
    :param nexus_url: The Nexus base URL.
    :param organisation: The Nexus organisation.
    :param project: The Nexus project.
    :param token: The Nexus token.
    :param verify_ssl: If set to False, SSL verification will be disabled.
    :return: The schema creation response from Nexus.
    """

    try:
        req = requests.post(
            nexus_url + '/schemas/' + organisation + '/' + project,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }, data=json.dumps(schema), verify=verify_ssl)

        req.raise_for_status()

        return req.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            raise Exception(e.response.text)
        else:
            raise e

def get_composite_view(id: str, nexus_url: str, organisation: str, project: str, token: str, verify_ssl=True) -> Union[
    Dict, None]:
    """
    Given the id of a composite view, fetches it from Nexus.

    :param id: The composite view's id, e.g, connectome-projection-composite-01.
    :param nexus_url: The Nexus base URL.
    :param organisation: The Nexus organisation.
    :param project: The Nexus project.
    :param token: The Nexus token.
    :param verify_ssl: If set to False, SSL verification will be disabled.
    :return: The composite view fetched from Nexus or None if it does not exist.
    """

    try:
        req = requests.get(
            nexus_url + '/views/' + organisation + '/' + project + '/' + parse.quote_plus(id),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=verify_ssl
        )

        req.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            # Composite view was not found
            return None
        else:
            if e.response is not None:
                raise Exception(e.response.text)
            else:
                raise e

    return req.json()


def create_composite_view(composite_view: Dict, nexus_url: str, organisation: str, project: str, token: str,
                          verify_ssl=True) -> Dict:
    """
    Given a CompositeView, registers it in Nexus.

    :param composite_view: The new revision of the composite_view..
    :param nexus_url: The Nexus base URL.
    :param organisation: The Nexus organisation.
    :param project: The Nexus project.
    :param token: The Nexus token.
    :param verify_ssl: If set to False, SSL verification will be disabled.
    :return: The creation response from Nexus.
    """
    try:
        req = requests.post(
            nexus_url + '/views/' + organisation + '/' + project,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }, data=json.dumps(composite_view), verify=verify_ssl)

        req.raise_for_status()

        return req.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            raise Exception(e.response.text)
        else:
            raise e

def update_composite_view(composite_view: Dict, rev: int, nexus_url: str, organisation: str, project: str, token: str,
                          verify_ssl=True) -> Dict:
    """
    Given a CompositeView, updates it in Nexus.

    :param composite_view: The new revision of the composite_view.
    :param rev: The revision of the current composite view.
    :param nexus_url: The Nexus base URL.
    :param organisation: The Nexus organisation.
    :param project: The Nexus project.
    :param token: The Nexus token.
    :param verify_ssl: If set to False, SSL verification will be disabled.
    :return: The update response from Nexus.
    """

    # get composite view's id
    try:
        composite_view_id = composite_view['@id']
    except KeyError as e:
        raise Exception('No @id given in composite view')

    try:
        req = requests.put(
            nexus_url + '/views/' + organisation + '/' + project + '/' + parse.quote_plus(
                # TODO: adapt so it also works for global search (id has a different base path)
                nexus_url + '/resources/' + organisation + '/' + project + '/_/' + composite_view_id),
            params={'rev': rev},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            data=json.dumps(composite_view),
            verify=verify_ssl
        )

        req.raise_for_status()

        return req.json()

    except requests.exceptions.HTTPError as e:
        raise e
