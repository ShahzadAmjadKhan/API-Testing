from aloe import *
import logging
import os
import requests
from datetime import datetime
from requests import Session

ENVIRONMENT = os.environ['TEST_ENVIRONMENT']
# logger = logging.getLogger(__name__)


@before.all
def setup_logging():
    DEBUG_LEVEL = logging.getLevelName(os.environ.get('DEBUG_LEVEL','WARNING'))
    logging.basicConfig(level=DEBUG_LEVEL, format='[%(asctime)s %(levelname)s %(name)s %(funcName)s()]: %(message)s ')
    logging.info("Using settings: ENVIRONMENT: {}, DEBUG_LEVEL: {}".format(ENVIRONMENT, DEBUG_LEVEL))


@before.all
def init_session():
    world.session = Session()
    world.session.verify = False
    world.environment = ENVIRONMENT


@before.all
def suppress_urllib3_warnings():
    requests.packages.urllib3.disable_warnings()


@before.all
def say_hello():
    global test_start_time
    test_start_time = datetime.now()
    logging.info("Lettuce starting for API test at: {} ...".format(test_start_time))
    world.srv_ids = []


@after.all
def say_goodbye(total):
    duration = datetime.now() - test_start_time
    logging.info("Lettuce ending for API test at: {} - duration: {}".format(datetime.now(), duration))


@world.absorb
def get_srv_ids():
    return world.srv_ids
