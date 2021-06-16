from http import HTTPStatus

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def submit(system_stats, server_address):
    """
    Send current system statistics to provided endpoint.

    :param system_stats: Current system statistics
    :param server_address: address of the server collecting system stats
    :return: None
    :raises: requests.exceptions.ConnectionError
    """
    try:
        with requests.session() as session:
            session.mount(
                "http://",
                HTTPAdapter(
                    max_retries=Retry(
                        total=5,
                        connect=5,
                        redirect=10,
                        backoff_factor=0.5,
                        status_forcelist=[
                            HTTPStatus.REQUEST_TIMEOUT,  # HTTP 408
                            HTTPStatus.CONFLICT,  # HTTP 409
                            HTTPStatus.INTERNAL_SERVER_ERROR,  # HTTP 500
                            HTTPStatus.BAD_GATEWAY,  # HTTP 502
                            HTTPStatus.SERVICE_UNAVAILABLE,  # HTTP 503
                            HTTPStatus.GATEWAY_TIMEOUT  # HTTP 504
                        ]
                    )
                )
            )

            re = session.post(server_address, json=system_stats)
    except requests.exceptions.RequestException:
        print(re.status_code, re.reason)
        print(f"[{system_stats['time'][-1]}] "
              f"Could not update system statistics on {system_stats['name']}.")
    else:
        print(f"[{system_stats['time'][-1]}] "
              f"Updated system statistics on {system_stats['name']}.")

