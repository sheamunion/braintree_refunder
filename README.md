# braintree_refunder

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

## TODO

### Urgent & Important

- [x] User can choose environmetn, add API keys, and upload a source file in required format.
- [x] User can provide a U.S. phone number
- [x] User can receive an SMS notification when job is complete
- [x] User can download a valid output CSV with logs
- [x] braintree_refunder is hosted on AWS EC2
- [ ] User can upload a file with headers other than `id,amount`. ([`TransactionLoader` module](https://github.com/sheamunion/braintree_refunder/blob/master/refunder/transaction_loader.py))
- [ ] User is returned to form with specific feedback when an error occurs
  * i.e. a user provides invalid Braintree API keys and Braintree throws an Authorization Error
  * i.e. Braintree-caused errors [Down for maintenance](https://developers.braintreepayments.com/reference/general/exceptions/python#down-for-maintenance), [Server error](https://developers.braintreepayments.com/reference/general/exceptions/python#server-error), etc.
- [ ] When a transaction is successfully voided, the log should not return the transaction ID.
- [ ] User can upload files in .xls or .csv format.
- [ ] User should not receive an SMS notification if they did not provide a phone number.

### Important & Not urgent 
- [ ] User can enter a valid U.S. phone number in any format including, not limited to the following:
  * (xxx) xxx-xxxx
  * (xxx) xxxxxxx
  * xxx-xxx-xxxx
  * xxx.xxx.xxxx
  * +1xxx.xxx.xxx
- [ ] Add reddis and django-rq to handle refund job asynchronously.
  - [ ] After user clicks submit, Django returns a 200 and renders a "refunding status" page.
  - [ ] The "refunding status" page periodically pings an endpoint on the server which returns the progress of the job. When the job is complete, it returns a url where the log can be downloaded.
- [ ] Spruce up the f/e presentation and user experience.
- [ ] Create a Dockerfile and image.
  - [ ] Use the Docker image on the EC2 instance.
 
## Running the service on AWS EC2

Connect to AWS instance via SSH:

`ssh aws`

_The config for this ssh command is in ~/.ssh/config._

Start nginx web server:

`sudo service nginx start`

Start the virutal environment:

`source /tmp/braintree_refunder/bin/activate`

Start gunicorn within virutal envionrment:

`gunicorn braintree_refunder.wsgi`

Navigate to [http://braintree-refunder.thoughtaware.com](http://braintree-refunder.thoughtaware.com)
