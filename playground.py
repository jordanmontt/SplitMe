import pandas
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from splitme import Ledger, CSVReader

columns_map = {
    "Date": "date",
    "Amount": "amount",
    "Currency": "currency",
    "Concept": "concept",
    "Involved": "participants",
    "Payer": "payer",
}
conversion_table = {
    "EUR": {"ALL": 100},
    "ALL": {"EUR": 0.01},
}

csv_file_path = Path.home() / "Documents" / "AlbaniaSplit" / "AlbaniaMerged.csv"
df = pandas.read_csv(
    csv_file_path, sep=";", comment="#", header=0, encoding="utf-8"
)
reader = CSVReader(df, columns_map)
expenses = reader.read()

ledger = Ledger(expenses=expenses, conversion_table=conversion_table)
balances = ledger.compute_balances()

for b in balances:
    print(b)
