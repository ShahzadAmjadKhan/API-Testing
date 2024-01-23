import json
import os
import threading

from aloe import step
from aloe import world
from requests import Response

BASE_URL = 'srv/sys/api'

@step('I call (\w+) "([^"]*)" with request "([^"]*)"')
def send_request_for_api(step, method, api, request_id):
    send_request(method, api, request_id)


@step('The response for (\w+) "([^"]*)" is "([^"]*)"')
def check_response(step, method, api, request_id):
    resp_json = json.loads(world.session.response.content)

    exp_resp = json.loads(get_message(request_id, method, api, False))

    assert resp_json['code'] == exp_resp['code'], \
        f"Got response: {resp_json['code']}, expected: {exp_resp['code']}"

    assert resp_json['message'] == exp_resp['message'],\
        f"Got response: {resp_json['message']}, expected: {exp_resp['message']}"

    assert resp_json['severity'] == exp_resp['severity'], \
        f"Got response: {resp_json['severity']}, expected: {exp_resp['severity']}"

    assert resp_json['innerErrors'][0]['code'] == exp_resp['innerErrors'][0]['code'], \
        f"Got response: {resp_json['innerErrors'][0]['code']}, expected: {exp_resp['innerErrors'][0]['code']}"

    assert resp_json['innerErrors'][0]['severity'] == exp_resp['innerErrors'][0]['severity'], \
        f"Got response: {resp_json['innerErrors'][0]['severity']}, expected: {exp_resp['innerErrors'][0]['severity']}"


@step('I call (\w+) "([^"]*)" with request "([^"]*)" (\d+) times using (\d+) threads expecting http codes "([^"]*)"')
def send_request_for_api(step, method, api, request_id, activity_count, thread_count, expected_http_codes_string):
    responses = world.client.parallel_tasks(activity_count, thread_count, send_request(method, api, request_id))
    assert_http_result_codes(responses, expected_http_codes_string)


def send_request(method, api, request_id):
    if request_id is not None:
        folder = api

        for p in api.split('/'):
            if p.isdigit():
                folder = folder.replace('/' + p, '')

        req = get_message(request_id, method, folder, True)
    else:
        req = ''

    if 'comments' in api.split('/'):
        api = api.replace('{serviceRequestId}', world.srv_ids[0])

    url = 'http://{}/{}/v1/{}'.format(world.environment, BASE_URL, api)

    request_headers = get_request_headers(req)

    request_body = get_request_body(req)

    print('url = ' + url)
    print('req = ' + req)

    if method.upper() == 'POST':
        world.session.response = world.session.post(url, data=request_body, headers=request_headers, timeout=10)

        if api == 'service-requests' and world.session.response.status_code == 201:
            header_location = world.session.response.headers['location']
            location = json.loads(world.session.response.content)['link']['href']
            assert header_location == location

            srv_id_start_index = location.rindex('/')
            world.srv_ids.append(location[srv_id_start_index+1:])

    print('response = ' + world.session.response.content)


def get_message(req_id, method, api_name, request=True):
    api_name = api_name.replace('{serviceRequestId}/', '')
    api_name = api_name.replace('/', '_')
    api_name = api_name.replace('-', '_')
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data', api_name, method)

    if request:
        ext = '.request'
    else:
        ext = '.response'

    with open(os.path.join(data_dir, req_id + ext), 'r') as ff:
        c = ff.read()

    return c


def get_request_headers(req):
    return json.loads(req)['request']['header']


def get_request_body(req):
    return json.dumps(json.loads(req)['request']['body'])


def parallel_tasks(self, invocation_count, thread_count, task):
        invocation_count_int = int(invocation_count)
        thread_count_int = int(thread_count)

        class ExecuteTasksThread (threading.Thread):
            def __init__(self, client, index):
                threading.Thread.__init__(self)
                self.client = client
                self.index = index
                self.results = []

            def run(self):
                iterations_in_this_thread = invocation_count_int / thread_count_int

                # Add remainder of division in some threads
                remainder = invocation_count_int % thread_count_int
                if self.index < remainder:
                    iterations_in_this_thread += 1

                for iteration_index in range(iterations_in_this_thread):
                    try:
                        self.results.append(task(self.client, '{}.{}'.format(self.index, iteration_index)))
                    except Exception as e:
                        self.results.append(e)

        threads = []

        # Create new threads
        for thread_id in range(thread_count_int):
            threads.append(ExecuteTasksThread(self.clone(), thread_id))

        # Start new Threads
        for thread in threads:
            thread.start()

        results = []

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            results.extend(thread.results)

        return results


def assert_http_result_codes(responses, expected_http_codes_string):
    only_responses = True
    for i in responses:
        if not type(i) == Response:
            only_responses = False
            print("Non-response in result: " + str(type(i)))
            print(str(i))

    assert only_responses, "Found non-responses"

    actual_http_codes = set(response.status_code for response in responses)
    expected_http_codes = set([int(http_code_string) for http_code_string in expected_http_codes_string.split(",")])

    assert expected_http_codes == actual_http_codes, \
        "Expected http codes {} but found {} (in {})".format(str(expected_http_codes),
                                                             str(actual_http_codes), str(responses))
