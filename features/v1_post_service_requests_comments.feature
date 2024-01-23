Feature: Add a new comment to the service request referred to by serviceRequestId

Scenario: 1 Successful call: post comments service request with valid data
  When I call POST "service-requests/{serviceRequestId}/comments" with request "v1_post_service_requests_comments1"
  Then the http status code is 201

Scenario: 2 Unsuccessful call: post service request with incomplete request body, commentText missing
  When I call POST "service-requests/{serviceRequestId}/comments" with request "v1_post_service_requests_comments2"
  Then the http status code is 400

Scenario: 3 Unsuccessful call: post service request with invalid request body, exposeEmployeeToClient invalid
  When I call POST "service-requests/{serviceRequestId}/comments" with request "v1_post_service_requests_comments3"
  Then the http status code is 400

Scenario: 4 Too Many Requests
  When I call POST "service-requests/{serviceRequestId}/comments" with request "v1_post_service_requests_comments1" 100 times using 25 threads expecting http codes "201,429"