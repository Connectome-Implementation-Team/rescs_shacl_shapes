import requests
from typing import Dict, Union


def get_composite_view(id: str, nexus_url: str, organisation: str, project: str, token: str, verify_ssl=True) -> Union[Dict, None]:
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
            print(e)
            return None
        else:
            raise Exception(e.response.text)



    return req.json()
