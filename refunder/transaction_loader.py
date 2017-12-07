import csv

class TransactionLoader():

    def __init__(self, source_file):
        self.source_file = source_file

    def all(self):
        txns = []
        reader = csv.DictReader(self.source_file)

        for row in reader:
            txns.append(row)

        return txns
