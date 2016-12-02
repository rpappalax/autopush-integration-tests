import os
import pytest
import requests
from ticket_helper import format_results


# TODO: add conditional to check for:
# a) env var
# b) an input var
# c) nuthin

TICKET_NUM = None

try:
    TICKET_NUM = os.environ['TICKET_NUM']
except KeyError:
    print('no TICKET_NUM indicated. printing results to stdout.')

def api_response(variables, path):
    URL = 'https://{0}/{1}'.format(variables['HOST_UPDATES'], path)
    return requests.get(URL)


def ticket_update(name_test, status):
    comments = format_results(name_test, status)
    print(comments)


@pytest.mark.nondestructive
def test_status_check(variables, request):
    name_test = request.node.name
    status = api_response(variables, 'status').json()
    assert('OK' == status['status'])
    assert(variables['VERSION'] == status['version'])
    if TICKET_NUM:
        ticket_update(name_test, status)


@pytest.mark.nondestructive
def test_health_check(variables, request):
    name_test = request.node.name
    r = api_response(variables, 'health')
    status = r.json()
    ROUTER = variables['ROUTER']
    STORAGE = variables['STORAGE']

    assert(0 == status['clients'])
    assert('OK' == status[ROUTER]['status'])
    assert('OK' == status[STORAGE]['status'])
    assert('OK' == status['status'])
    assert(variables['VERSION'] == status['version'])
    if TICKET_NUM:
        ticket_update(name_test, status)
