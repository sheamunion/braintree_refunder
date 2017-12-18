# TODO

## Urgent & Important

- [x] User can choose environmetn, add API keys, and upload a source file in required format.
- [x] User can provide a U.S. phone number
- [x] User can download a valid output CSV with logs
- [x] braintree_refunder is hosted on AWS EC2
- [ ] User can receive an SMS notification when job is complete
  * [ ] Add tests for SMS story
- [ ] User can upload a file with headers other than `id,amount`. ([`TransactionLoader` module](https://github.com/sheamunion/braintree_refunder/blob/master/refunder/transaction_loader.py))
- [ ] User is returned to form with specific feedback when an error occurs
  * i.e. a user provides invalid Braintree API keys and Braintree throws an Authorization Error
  * i.e. Braintree-caused errors [Down for maintenance](https://developers.braintreepayments.com/reference/general/exceptions/python#down-for-maintenance), [Server error](https://developers.braintreepayments.com/reference/general/exceptions/python#server-error), etc.
- [ ] When a transaction is successfully voided, the log should not return the transaction ID.
- [ ] User can upload files in .xls or .csv format.
- [ ] User should not receive an SMS notification if they did not provide a phone number.

## Important & Not urgent 
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
