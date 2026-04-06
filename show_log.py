import pandas as pd

df = pd.read_parquet("Log.parquet")
print(df.to_string())
