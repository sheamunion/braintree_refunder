# braintree_refunder

Refund a list of transaction IDs from a CSV using the Braintree API

## Running the service on AWS EC2

ssh to AWS instance:

`ssh aws`

_The config for this ssh command is in ~/.ssh/config._

Start nginx web server:

`sudo service nginx start`

Start the virutal environment:

`source /tmp/braintree_refunder/bin/activate`

Start gunicorn within virutal envionrment:

`gunicorn braintree_refunder.wsgi`

Navigate to the [http://braintree-refunder.thoughtaware.com](http://braintree-refunder.thoughtaware.com)
