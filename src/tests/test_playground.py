import unittest
import pandas
from pathlib import Path
from splitme import CSVReader, Ledger

"""Testing my personal csv file"""


class TestCSVReader(unittest.TestCase):

    def setUp(self):
        columns_map = {
            "Date": "date",
            "Amount": "amount",
            "Currency": "currency",
            "Concept": "concept",
            "Involved": "participants",
            "Payer": "payer",
        }
        conversion_table = {
            "EUR": {"ALL": 100},
            "ALL": {"EUR": 0.01},
        }
        
        csv_file_path = Path.home() / "Documents" / "AlbaniaSplit" / "AlbaniaMerged.csv"
        self.df = pandas.read_csv(
            csv_file_path, sep=";", comment="#", header=0, encoding="utf-8"
        )
        self.reader = CSVReader(self.df, columns_map)
        self.expenses = self.reader.read()
        
        self.ledger = Ledger(expenses=self.expenses, conversion_table=conversion_table)
        balances = self.ledger.compute_balances()

    def test_csv_file_properties(self):
        valid_people = {"S", "A", "P"}

        for expense in self.expenses:
            self.assertTrue(
                set(expense.participants).issubset(valid_people),
                f"Invalid participants found: {expense.participants}",
            )
            self.assertIsNotNone(expense.payer, "Missing payer")
            self.assertIn(
                expense.payer, valid_people, f"Invalid payer found: {expense.payer}"
            )
            self.assertIsInstance(expense.amount, float)
            self.assertLessEqual(expense.amount, 110)
            self.assertGreater(
                expense.amount, 0, f"Non-positive amount: {expense.amount}"
            )

            self.assertIsInstance(expense.concept, str)
            self.assertTrue(expense.concept.strip(), "Empty concept found")


if __name__ == "__main__":
    unittest.main()
