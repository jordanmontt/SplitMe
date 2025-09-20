from .ExpenseParser import ExpenseParser


class CSVReader:
    def __init__(self, df):
        self.set_up_df(df)
        self.expenses = []
        self.set_up_columns_map(
            {
                "Date": "date",
                "Amount": "amount",
                "Currency": "currency",
                "Concept": "concept",
                "Involved": "participants",
                "Payer": "payer",
            }
        )

    def __init__(self, df, columns_map):
        self.set_up_df(df)
        self.expenses = []
        self.set_up_columns_map(columns_map)

    def set_up_df(self, df):
        self.df = df

    def set_up_columns_map(self, a_dict):
        self.columns_map = a_dict

    def map_column_names(self):
        self.df = self.df.rename(columns=self.columns_map)

    def read(self):
        self.map_column_names()

        self.expenses = ExpenseParser().parse_expenses(self.df.to_dict("records"))
        return self.expenses
