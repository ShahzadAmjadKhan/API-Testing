# API-Testing
A python project to test APIs based on feature files with predefined requests and response to verify

data folder contains request and responses to be matched 
features folder contains the BDD feature files containing different scenario to be tested for API
step folder contains python based step definitions to execute the tests

# How to Run
Define an environment variable 'TEST_ENVIRONMENT' containing the base URL for api e.g. https://selfhost.test/app
lettuce <feature file>
