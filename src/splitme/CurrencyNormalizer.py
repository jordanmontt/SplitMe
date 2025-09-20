from abc import ABC, abstractmethod


class Currency(ABC):
    def __init__(self, amount: float = None, conversion_table: dict = None):
        self._init_defaults()

        if amount is not None:
            self.amount = amount
        if conversion_table is not None:
            self.conversion_table = conversion_table
            
    def _init_defaults(self):
        self.code = None
        self.amount = 0.0
        self.conversion_table = {}
    
    
    @classmethod
    def new_currency(self, amount, code, conversion_table):
        if (code == "EUR"):
            return EUR(amount, conversion_table)
        if (code == "ALL"):
            return ALL(amount, conversion_table)
        
    @abstractmethod
    def to_eur(self):
        pass
    
    @abstractmethod
    def to_all(self):
        pass
    

class EUR(Currency):

    def _init_defaults(self):
        super()._init_defaults()
        self.code = "EUR"
    

    def to_eur(self):
        return self
    
    def to_all(self):
        rate = self.conversion_table[self.code][ALL().code]
        return ALL(self.amount * rate)


class ALL(Currency):
    
    def _init_defaults(self):
        super()._init_defaults()
        self.code = "ALL"
    
    
    def to_all(self):
        return self
    
    def to_eur(self):
        rate = self.conversion_table[self.code][EUR().code]
        return EUR(self.amount * rate)


class CurrencyNormalizer:
    
    def __init__(self, expenses, conversion_table):
        self.expenses = expenses
        self.conversion_table = conversion_table
    
    
    def normalize_currencies(self):
        for expense in self.expenses:
            currency_object = Currency.new_currency(expense.amount, expense.currency, self.conversion_table)
            expense.amount = currency_object.to_eur().amount
        return self.expenses