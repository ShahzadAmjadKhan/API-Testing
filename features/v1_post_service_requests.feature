Feature: Create a new service request

Scenario: 1 Successful call: post habits service request with valid data
  When I call POST "service-requests" with request "v1_post_service_requests1"
  Then the http status code is 201

Scenario: 2 Unsuccessful call: post habits service request with invalid header, sendingPartyId missing
  When I call POST "service-requests" with request "v1_post_service_requests2"
  Then the http status code is 400
  And the response for POST "service-requests" is "v1_post_service_requests2"

Scenario: 3 Unsuccessful call: post habits service request with incomplete request body, partyId and grid missing
  When I call POST "service-requests" with request "v1_post_service_requests3"
  Then the http status code is 400
  And the response for POST "service-requests" is "v1_post_service_requests3"

Scenario: 4 Unsuccessful call: post habits service request with invalid request body, partyId invalid
  When I call POST "service-requests" with request "v1_post_service_requests4"
  Then the http status code is 400
  And the response for POST "service-requests" is "v1_post_service_requests4"

Scenario: 5 Unsuccessful call: post habits service request with invalid request body, dob invalid
  When I call POST "service-requests" with request "v1_post_service_requests5"
  Then the http status code is 400
  And the response for POST "service-requests" is "v1_post_service_requests5"

Scenario: 6 Unsuccessful call: post habits service request with invalid request body, dueDate invalid
  When I call POST "service-requests" with request "v1_post_service_requests6"
  Then the http status code is 400
  And the response for POST "service-requests" is "v1_post_service_requests6"

Scenario: 7 Too Many Requests habits
  When I call POST "service-requests" with request "v1_post_service_requests1" 100 times using 25 threads expecting http codes "201,429"

Scenario: 8 Successful call: post SEPA Recall Consent request with valid data
  When I call POST "service-requests" with request "v1_post_service_requests7"
  Then the http status code is 201