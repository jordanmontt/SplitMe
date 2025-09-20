import unittest
import pandas
from pathlib import Path
from splitme import CSVReader


class TestCSVReader(unittest.TestCase):

    def setUp(self):
        self.data = {
            "Date": ["2/09/25", "02/09/25", "02/09/25"],
            "Amount": ["50", "5000", "7,5"],
            "Currency": ["eur", "all", "eur"],
            "Concept": ["hostel", "food", "gas"],
            "Involved": ["S, P, A", "S, A, P", "S, A, P"],
            "Payer": ["A", "P", "S"],
        }
        columns_map = {
            "Date": "date",
            "Amount": "amount",
            "Currency": "currency",
            "Concept": "concept",
            "Involved": "participants",
            "Payer": "payer",
        }

        self.df = pandas.DataFrame(self.data)
        self.reader = CSVReader(self.df, columns_map)
        self.expenses = self.reader.read()

    def test_csvreader_sample_data(self):
        self.assertEqual(len(self.expenses), 3)

        self.assertEqual(self.expenses[0].amount, 50)
        self.assertEqual(self.expenses[1].amount, 5000)
        self.assertEqual(self.expenses[2].amount, 7.5)
        
        self.assertEqual(self.expenses[0].currency, "EUR")
        self.assertEqual(self.expenses[1].currency, "ALL")
        self.assertEqual(self.expenses[2].currency, "EUR")

        self.assertEqual(self.expenses[0].participants, ["S", "P", "A"])
        self.assertEqual(self.expenses[1].participants, ["S", "A", "P"])
        self.assertEqual(self.expenses[2].participants, ["S", "A", "P"])

        self.assertEqual(self.expenses[0].payer, "A")
        self.assertEqual(self.expenses[1].payer, "P")
        self.assertEqual(self.expenses[2].payer, "S")


if __name__ == "__main__":
    unittest.main()
