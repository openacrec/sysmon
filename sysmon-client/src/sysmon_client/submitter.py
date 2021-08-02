from http import HTTPStatus
from typing import Dict, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def check_address(url: str) -> str:
    """For now, remove trailing / if there is one."""
    if url.endswith("/"):
        return url[0:-1]
    return url


# Seperated from continues_submit() for testing purposes.
def submit(json_data: Dict[str, Any], full_address: str):
    """
    General submission function to send json data to a remote endpoint.

    :param json_data: Current system statistics
    :param full_address: address of the server with attached endpoint
    :return:
    :raises: requests.exceptions.ConnectionError
    """
    with requests.session() as session:
        session.mount(
            "http://",
            HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    connect=5,
                    redirect=10,
                    backoff_factor=0.2,
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

        session.post(full_address, json=json_data)


def continues_submit(system_stats: Dict[str, Any], server_address: str):
    """
    Execute the submit function in a try except block in order for it
    to always continue operation.

    :param system_stats: Current system statistics
    :param server_address: address of the server collecting system stats
    :return:
    """
    server_address = check_address(server_address)
    try:
        submit(system_stats, f"{server_address}/api/v01")
    except requests.exceptions.RequestException:
        print(f"[{system_stats['time']}] "
              f"Could not update system statistics on {system_stats['name']}.")

    else:
        print(f"[{system_stats['time']}] "
              f"Updated system statistics on {system_stats['name']}.")


def request_deletion(system_stats: Dict[str, Any], server_address: str):
    """
    Send this machine's name to the deletion endpoint of the sysmon server.

    :param system_stats: Current system statistics
    :param server_address: address of the server collecting system stats
    :return:
    """
    server_address = check_address(server_address)
    to_delete = {"name": system_stats["name"]}
    submit(to_delete, f"{server_address}/api/del")


def send_task_status(task_status: Dict[str, Any], server_address: str):
    """
    Send the current status of task execution to the executions endpoint.

    :param task_status: JSON containing information about current task status.
    :param server_address: address of the server collecting this status
    :return:
    """
    server_address = check_address(server_address)
    submit(task_status, f"{server_address}/api/executions")
