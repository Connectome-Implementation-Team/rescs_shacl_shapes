import requests
from typing import Dict, Union
from urllib import parse
import json

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
            nexus_url + '/views/' + organisation + '/' + project + '/' + id,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            verify=verify_ssl
        )

        req.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # Composite view was not found
            return None
        else:
            raise Exception(e.response.text)

    return req.json()


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
    """

    # get composite view's id
    try:
        composite_view_id = composite_view['@id']
    except KeyError as e:
        raise Exception('No @id given in composite view')

    try:
        req = requests.put(
            nexus_url + '/views/' + organisation + '/' + project + '/' + parse.quote_plus(
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
