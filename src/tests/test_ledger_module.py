import unittest
import pandas as pd
from splitme import Ledger, ExpenseParser


class TestLedger(unittest.TestCase):

    def setUp(self):
        raw_data = [
            ["2/09/25", "50", "hostel", "S, P, A", "A"],
            ["02/09/25", "5000 lek", "food", "S, P", "P"],
            ["02/09/25", "30", "gas", "S, A, P", "S"],
            ["05/09/25", "500 lek", "ensalada", "S", "A"],
            ["06/09/25" ,"20", "propina hostel", "S, A, P", "S"],
            ["06/09/25", "60", "almuerzo saranda", "S, A, P", "S"],
            ["07/09" ,"2000 lek", "Futbol", "S, P", "P"],
            ["07/09", "90", "Bote", "S, P, A", "P"],
            ["07/09", "7", "Chela noche", "P, A", "P"],
            ["07/09", "1500 lek", "Rancho cerro (45 euros)", "A, S, P", "A"] 
        ]
        self.expenses = ExpenseParser().parse_expenses(raw_data)


    def test_simple_balances(self):
        raw_data = [
            ["2/09/25", "50", "hostel", "S, P, A", "A"],
            ["02/09/25", "5000 lek", "food", "S, P, A", "P"],
        ]
        self.expenses = ExpenseParser().parse_expenses(raw_data)
    
        ledger = Ledger(self.expenses)
        balances = ledger.compute_balances()

        personA = next((b for b in balances if b.debitor == "A"), None)
        personP = next((b for b in balances if b.debitor == "P"), None)
        personS = next((b for b in balances if b.debitor == "S"), None)
        
        self.assertAlmostEqual(personS.total_debt(), 16.6667 + 16.6667, places=2)
        self.assertAlmostEqual(personS.debt_to("A"), 16.6667, places=2)
        self.assertAlmostEqual(personS.debt_to("P"), 16.6667, places=2)
    
        self.assertAlmostEqual(personP.debt_to("A"), 16.6667, places=2)
        self.assertAlmostEqual(personA.debt_to("P"), 16.6667, places=2)

    def test_ledger_balances(self):
        ledger = Ledger(self.expenses)
        balances = ledger.compute_balances()

        personA = next((b for b in balances if b.debitor == "A"), None)
        personP = next((b for b in balances if b.debitor == "P"), None)
        personS = next((b for b in balances if b.debitor == "S"), None)
        
        self.assertAlmostEqual(personS.total_debt(), 16.6667 + 25 + 5 + 10 + 30 + 5, places=2)
        self.assertAlmostEqual(personS.debt_to("A"), 16.6667 + 5 + 5, places=2)
        self.assertAlmostEqual(personS.debt_to("P"), 25 + 10 + 30, places=2)
    
        self.assertAlmostEqual(personP.total_debt(), 16.6667 +  10 + 6.6667 + 20 + 5, places=2)
        self.assertAlmostEqual(personP.debt_to("A"), 16.6667 + 5, places=2)
        self.assertAlmostEqual(personP.debt_to("S"), 10 + 6.6667 + 20, places=2)
        
        self.assertAlmostEqual(personA.debt_to("S"), 10 + 6.666667 + 20, places=2)
        self.assertAlmostEqual(personA.debt_to("P"), 30 + 3.5, places=2)
        self.assertAlmostEqual(personA.total_debt(), 10 + 6.666667 + 20 + 30 + 3.5, places=2)
      
        

    def test_borrow_money(self):
        raw_data = [ ["05/09/25", "500 lek", "ensalada", "S", "A"] ]
        self.expenses = ExpenseParser().parse_expenses(raw_data)
        ledger = Ledger(self.expenses)
        balances = ledger.compute_balances()
        personS = next((b for b in balances if b.debitor == "S"), None)
        assert personS.debt_to("A") == 5


if __name__ == "__main__":
    unittest.main()
