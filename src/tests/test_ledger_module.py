import unittest
import pandas
from splitme import Ledger, CSVReader, ExpenseParser


class TestLedger(unittest.TestCase):

    def setUp(self):
        raw_data = [
            ["2/09/25", "50", "eur", "hostel", "S, P, A", "A"],
            ["02/09/25", "5000", "all", "food", "S, P", "P"],
            ["02/09/25", "30", "eur", "gas", "S, A, P", "S"],
            ["05/09/25", "500", "all", "ensalada", "S", "A"],
            ["06/09/25", "20", "eur", "propina hostel", "S, A, P", "S"],
            ["06/09/25", "60", "eur", "almuerzo saranda", "S, A, P", "S"],
            ["07/09", "2000", "all", "Futbol", "S, P", "P"],
            ["07/09", "90", "eur", "Bote", "S, P, A", "P"],
            ["07/09", "7", "eur", "Chela noche", "P, A", "P"],
            ["07/09", "1500", "all", "Rancho cerro (45 euros)", "A, S, P", "A"],
        ]
        self.header = ["Date", "Amount", "Currency", "Concept", "Involved", "Payer"]
        self.columns_map = {
            "Date": "date",
            "Amount": "amount",
            "Currency": "currency",
            "Concept": "concept",
            "Involved": "participants",
            "Payer": "payer",
        }
        self.conversion_table = {
            "EUR": {"ALL": 100},
            "ALL": {"EUR": 0.01},
        }

        self.df = pandas.DataFrame(raw_data, columns=self.header)
        self.reader = CSVReader(self.df, self.columns_map)
        self.expenses = self.reader.read()
        self.ledger = Ledger(expenses=self.expenses, conversion_table=self.conversion_table)

    def test_simple_balances(self):
        header = ["Date", "Amount", "Concept", "Involved", "Payer", "Currency"]
        raw_data = [
            ["2/09/25", "50", "hostel", "S, P, A", "A", "eur"],
            ["02/09/25", "5000", "food", "S, P, A", "P", "all"],
        ]
        self.df = pandas.DataFrame(raw_data, columns=header)
        self.expenses = CSVReader(self.df, self.columns_map).read()
        self.ledger.expenses = self.expenses
    
        balances = self.ledger.compute_balances()

        personA = next((b for b in balances if b.debitor == "A"), None)
        personP = next((b for b in balances if b.debitor == "P"), None)
        personS = next((b for b in balances if b.debitor == "S"), None)

        self.assertAlmostEqual(personS.total_debt(), 16.6667 + 16.6667, places=2)
        self.assertAlmostEqual(personS.debt_to("A"), 16.6667, places=2)
        self.assertAlmostEqual(personS.debt_to("P"), 16.6667, places=2)

        self.assertAlmostEqual(personP.debt_to("A"), 16.6667, places=2)
        self.assertAlmostEqual(personA.debt_to("P"), 16.6667, places=2)

    def test_ledger_balances(self):
        balances = self.ledger.compute_balances()

        personA = next((b for b in balances if b.debitor == "A"), None)
        personP = next((b for b in balances if b.debitor == "P"), None)
        personS = next((b for b in balances if b.debitor == "S"), None)

        self.assertAlmostEqual(
            personS.total_debt(), 16.6667 + 25 + 5 + 10 + 30 + 5, places=2
        )
        self.assertAlmostEqual(personS.debt_to("A"), 16.6667 + 5 + 5, places=2)
        self.assertAlmostEqual(personS.debt_to("P"), 25 + 10 + 30, places=2)

        self.assertAlmostEqual(
            personP.total_debt(), 16.6667 + 10 + 6.6667 + 20 + 5, places=2
        )
        self.assertAlmostEqual(personP.debt_to("A"), 16.6667 + 5, places=2)
        self.assertAlmostEqual(personP.debt_to("S"), 10 + 6.6667 + 20, places=2)

        self.assertAlmostEqual(personA.debt_to("S"), 10 + 6.666667 + 20, places=2)
        self.assertAlmostEqual(personA.debt_to("P"), 30 + 3.5, places=2)
        self.assertAlmostEqual(
            personA.total_debt(), 10 + 6.666667 + 20 + 30 + 3.5, places=2
        )

    def test_borrow_money(self):
        header = ["Date", "Amount", "Concept", "Involved", "Payer", "Currency"]
        raw_data = [["05/09/25", "500", "ensalada", "S", "A", "all"]]
        self.df = pandas.DataFrame(raw_data, columns=header)
        self.expenses = CSVReader(self.df, self.columns_map).read()
        self.ledger.expenses = self.expenses

        balances = self.ledger.compute_balances()
        personS = next((b for b in balances if b.debitor == "S"), None)
        assert personS.debt_to("A") == 5


if __name__ == "__main__":
    unittest.main()
