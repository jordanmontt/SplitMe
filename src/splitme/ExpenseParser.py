class Expense:
    def __init__(self, date, amount, concept, participants, payer, currency):
        self.date = date
        self.amount = amount
        self.concept = concept
        self.participants = participants
        self.payer = payer
        self.currency = currency


class ExpenseParser:
    
    def __init__(self):
        self.LEK_TO_EUR = 100

    def parse_expense(self, expense_as_dict):
        date = expense_as_dict["date"]
        amount = expense_as_dict["amount"]
        concept = expense_as_dict["concept"]
        participants= expense_as_dict["participants"]
        payer = expense_as_dict["payer"]
        currency = expense_as_dict["currency"]
    
        return Expense(date=date, amount=self.parse_amount(amount), currency=(self.parse_currency(currency)), concept=concept,
                       participants=self.parse_participants(participants), payer=self.parse_payer(payer))

    def parse_expenses(self, expenses_as_dict):
        self.expenses = [ self.parse_expense(expense_as_dict) for expense_as_dict in expenses_as_dict ]
        return self.expenses

    def parse_amount(self, amount_as_string):
        # parsed_amount = str(amount_as_string).strip().lower().replace(",", ".")
        # num = float("".join(ch for ch in parsed_amount if ch.isdigit() or ch == "."))
        # if "lek" in parsed_amount:
        #     return num / self.LEK_TO_EUR
        # return num
        parsed_amount = str(amount_as_string).strip().replace(",", ".")
        return float(parsed_amount)

    def parse_participants(self, row):
        return [ p.strip() for p in row.split(",") ]
    
    def parse_currency(self, currency):
        return str(currency).strip().upper()

    def parse_payer(self, row):
        return str(row)
        