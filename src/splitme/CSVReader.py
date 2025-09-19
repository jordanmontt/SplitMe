from .ExpenseParser import ExpenseParser


class CSVReader:
    def __init__(self, df):
       self.df = df
       self.expenses = []
    
    def read(self):
        self.expenses = ExpenseParser().parse_expenses(self.df.values.tolist())
        return self.expenses