class Expense:
    def __init__(self, date, amount, concept, participants, payer):
        self.date = date
        self.amount = amount
        self.concept = concept
        self.participants = participants
        self.payer = payer


class ExpenseParser:
    
    def __init__(self):
        self.LEK_TO_EUR = 100

    def parse_expense(self, raw_expense):
        return Expense(raw_expense[0], self.parse_amount(raw_expense[1]), raw_expense[2], 
                       self.parse_participants(raw_expense[3]), self.parse_payer(raw_expense[4]))

    def parse_expenses(self, raw_expenses):
        self.expenses = [ self.parse_expense(expense) for expense in raw_expenses ]
        return self.expenses

    def parse_amount(self, amount_as_string):
        parsed_amount = str(amount_as_string).strip().lower().replace(",", ".")
        num = float("".join(ch for ch in parsed_amount if ch.isdigit() or ch == "."))
        if "lek" in parsed_amount:
            return num / self.LEK_TO_EUR
        return num

    def parse_participants(self, row):
        return [ p.strip() for p in row.split(",") ]

    def parse_payer(self, row):
        return str(row)
        