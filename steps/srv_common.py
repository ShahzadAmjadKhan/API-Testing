import os
from aloe import *

ENVIRONMENT = os.environ['TEST_ENVIRONMENT']


@step('The http status code is (\d+)')
def http_status_code(step, status_code):
    assert world.session.response.status_code == int(status_code), \
        "status code should be {} but was {}".format(status_code, world.session.response.status_code)

