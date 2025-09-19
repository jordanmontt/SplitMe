import pandas
from pathlib import Path
from splitme import Ledger, CSVReader

csv_file_path = Path.home() / "Documents" / "AlbaniaSplit" / "AlbaniaMerged.csv"
df = pandas.read_csv(csv_file_path, sep=";", comment="#", header=0, encoding="utf-8")

expenses = CSVReader(df).read()
ledger = Ledger(expenses)
balances = ledger.compute_balances()

for b in balances:
    print(b)