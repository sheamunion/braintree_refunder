import braintree
from braintree.environment import Environment

class BraintreeRefundGateway():

    def __init__(self, keys):
        try: 
            self.__create_gateway(keys)
        except braintree.exceptions.authentication_error.AuthenticationError as e:
            return e

    def __create_gateway(self, keys):
        braintree.Configuration.configure(
            self.__get_env(keys[0]),
            keys[1],
            keys[2],
            keys[3]
        )        
        if not self.__has_valid_keys():
            raise braintree.exceptions.authentication_error.AuthenticationError
        return 

    def __get_env(self, key):
        if key == 'sandbox':
            return braintree.Environment.Sandbox
        else:
            return braintree.Environment.Production

    def __has_valid_keys(self):
        try:
            braintree.ClientToken.generate()
            return True
        except braintree.exceptions.authentication_error.AuthenticationError as e:
            return False

    def find_void_or_refund(self, txn_dict):
        txn_id     = txn_dict['id']
        txn_amount = txn_dict['amount']

        txn_find_result = self.find(txn_id)
        
        if type(txn_find_result) is not braintree.transaction.Transaction:
            return txn_find_result

        if self.is_voidable(txn_find_result):
            result = self.void(txn_id)
        elif self.is_refundable(txn_find_result):
            result = self.refund(txn_id, txn_amount)
        else:
            result = [txn_id, '', 'NO OPERATION', 'Transaction must have a status in "Authorized, Submitted For Settlement, Settlement Pending, Settling, or Settled."']
        return result

    def find(self, txn_id):
        try:
            return braintree.Transaction.find(txn_id)
        except braintree.exceptions.not_found_error.NotFoundError as e:
            return [txn_id, '', 'NOT FOUND', 'Transaction does not exist.']

    def is_voidable(self, txn):
        VOIDABLE_STATUSES_FOR_CARDS  = ['authorized', 'submitted_for_settlement']
        VOIDABLE_STATUSES_FOR_PAYPAL = ['settlement_pending'] + VOIDABLE_STATUSES_FOR_CARDS

        if txn.payment_instrument_type == 'paypal_account':
           return True if txn.status in VOIDABLE_STATUSES_FOR_PAYPAL else False
        
        return True if txn.status in VOIDABLE_STATUSES_FOR_CARDS else False
         
    def void(self, txn_id):
        result = braintree.Transaction.void(txn_id)

        if result.is_success:
            return [txn_id, result.transaction.id, 'SUCCESS', 'Transaction voided.']
        else:
            return [txn_id, '', 'FAILURE', result.message]

    def is_refundable(self, txn):
        REFUNDABLE_STATUSES = ['settled', 'settling']
        return True if txn.status in REFUNDABLE_STATUSES else False

    def refund(self, txn_id, amount):
        result = braintree.Transaction.refund(txn_id, amount)
        if result.is_success:
            return [txn_id, result.transaction.id, 'SUCCESS', 'Transaction refunded.']
        else:
            return [txn_id, '', 'FAILURE', result.message]

