class Balance:
    def __init__(self, debitor):
        self.debitor = debitor
        self.creditors = {}

    def add_debt(self, amount, creditor):
        self.creditors[creditor] = self.creditors.get(creditor, 0) + amount

    def total_debt(self):
        return sum(self.creditors.values())

    def debt_to(self, creditor):
        return self.creditors.get(creditor, 0)
    
    def substract_debt(self, creditor, amount):
        self.creditors[creditor] -= amount

    def __repr__(self):
        creditors_str = ", ".join([f"{c}: {amt:.2f}" for c, amt in self.creditors.items()])
        return f"Balance(debitor={self.debitor}, total={self.total_debt():.2f}, creditors={{ {creditors_str} }})"




class Ledger:
    def __init__(self, expenses):
        self.expenses = expenses
        self.balances = {}

    def get_balance_of(self, person):
        return self.balances.setdefault(person, Balance(person))
    
    
    def compute_balances(self):
        for expense in self.expenses:
            payer = expense.payer
            share = expense.amount / len(expense.participants)
            for participant in expense.participants:
                if participant != payer:
                    balance = self.get_balance_of(participant)
                    balance.add_debt(share, payer)
        return self.balances.values()