# braintree_refunder

## Table of Contents

* [Purpose](#purpose)
* [Input](#input)
* [Output](#output)
* [Contributing](#contributing)
* [TODO](#todo)
* [Requirements](#requirements)
* [Run the project locally](#run-the-project-locally)
* [Run the tests](#run-the-tests)

## Purpose:

Automatically void or refund Braintree transactions.

## Input

1. **[required]** [Sandbox or Production API keys](https://articles.braintreepayments.com/control-panel/important-gateway-credentials#api-keys) for a user with API access _and_ the following permissions:
* Credit Previous Transactions (Refunds)
* Void Transactions

2. **[required]** A CSV file that includes a header, Braintree transaction IDs, and, optionally, the amount to refund.

| id | amount |
| :--- | ---: |
| de48m2c7 | 3.50 |
| c929kphn | |
| jn3g8509 | |
| 1geft1mj | 1,000,000 |
| rqgqy6yn | |

3. _[optional]_ A valid U.S. phone number to receive an SMS notification when the job is complete.

## Output

1. A CSV formatted file that logs the result of every attempted void or refund.

| transaction_id | refunded_transaction_id | status | message | 
| --- | --- | --- | --- |
| de48m2c7  |  | FAILURE | Credit transactions cannot be refunded. |
| c929kphn  |  | FAILURE | Transaction has already been completely refunded. |
| jn3g8509 | | NO OPERATION | Transaction must have a status in "Authorized, Submitted For Settlement, Settlement Pending, Settling, or Settled." |
| 1geft1mj | 1geft1mj | SUCCESS | Transaction voided. |
| rqgqy6yn | qweby7pq | SUCCESS | Transaction refunded. |

2. _If phone number was provided_, an SMS notification.

## Contributing

See [CONTRIBUTING.md](https://github.com/sheamunion/braintree_refunder/blob/master/CONTRIBUTING.md).

## TODO

See [TODO.md](https://github.com/sheamunion/braintree_refunder/blob/master/TODO.md).

## Requirements

* Python3
* pip3
* Django
* Chrome web driver. [Get it here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
* An APP_SECRET_KEY. [From the Django docs](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECRET_KEY), "A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value." [Follow these instructions](https://stackoverflow.com/a/16630719/5326365) to generate an `APP_SECRET_KEY`.
* Braintree [Sandbox or Production API keys](https://articles.braintreepayments.com/control-panel/important-gateway-credentials#api-keys)
* Twilio SID and Token. Find these in [your Twilio account](https://twilio.com/user/account).

## Run the project locally

1. Clone the repo.
2. Create a virtual environment
```
python3 -m venv venv
```
3. Activate the venv
```
source venv/bin/activate
```
4. Install requirements
```
pip3 install -r requirements.txt
```
5. Copy example.env file to .env file in project root and add keys.
* See [requirements](#requirements)
6. Create a `files` directory in the `refunder/` app.
```
mkdir refunder/files
```
7. Run the development server
```
python3 manage.py runserver
```

## Run the tests

1. Run the development server.
```
python3 manage.py runserver
```
2. Run the functional tests.
```
python3 manage.py test functional_tests
```
3. Run the unit tests
```
python3 manage.py test refunder
```
4. Run unit tests for a specific module
```
python3 manage.py test refunder.test_module_name
``` 
