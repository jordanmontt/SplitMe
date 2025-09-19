import unittest
import pandas
from pathlib import Path
from splitme import CSVReader


class TestCSVReader(unittest.TestCase):

    def setUp(self):
        self.data = {
            "Fecha": ["2/09/25", "02/09/25", "02/09/25"],
            "Monto (euros)": ["50", "5000 lek", "7,5"],
            "Concepto": ["hostel", "food", "gas"],
            "Quienes": ["S, P, A", "S, A, P", "S, A, P"],
            "Pago": ["A", "P", "S"]
        }
        self.df = pandas.DataFrame(self.data)
        self.reader = CSVReader(self.df)
        self.expenses = self.reader.read()


    def test_csvreader_sample_data(self):
        self.assertEqual(len(self.expenses), 3)

        self.assertEqual(self.expenses[0].amount, 50)
        self.assertEqual(self.expenses[1].amount, 5000 / 100)  # lek conversion
        self.assertEqual(self.expenses[2].amount, 7.5)

        self.assertEqual(self.expenses[0].participants, ["S", "P", "A"])
        self.assertEqual(self.expenses[1].participants, ["S", "A", "P"])
        self.assertEqual(self.expenses[2].participants, ["S", "A", "P"])

        self.assertEqual(self.expenses[0].payer, "A")
        self.assertEqual(self.expenses[1].payer, "P")
        self.assertEqual(self.expenses[2].payer, "S")


    def test_csv_file_properties(self):
        csv_file_path = Path.home() / "Documents" / "AlbaniaSplit" / "AlbaniaMerged.csv"
        self.df = pandas.read_csv(csv_file_path, sep=";", comment="#", header=0, encoding="utf-8")
        self.reader = CSVReader(self.df)
        self.expenses = self.reader.read()
        
        
        valid_people = {"S", "A", "P"}

        for expense in self.expenses:
            self.assertTrue(
                set(expense.participants).issubset(valid_people),
                f"Invalid participants found: {expense.participants}"
            )
            self.assertIsNotNone(expense.payer, "Missing payer")
            self.assertIn(
                expense.payer, valid_people,
                f"Invalid payer found: {expense.payer}"
            )        
            self.assertIsInstance(expense.amount, float)
            self.assertLessEqual(expense.amount, 110)
            self.assertGreater(expense.amount, 0, f"Non-positive amount: {expense.amount}")

            self.assertIsInstance(expense.concept, str)
            self.assertTrue(expense.concept.strip(), "Empty concept found")


if __name__ == "__main__":
    unittest.main()
