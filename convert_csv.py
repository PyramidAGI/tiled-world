import pandas as pd

csv_path = r"C:\Users\Pieter\Documents\AGI-26. San Francisco\tiled-world.csv"

df = pd.read_csv(csv_path, sep=";", dtype=str, keep_default_na=False)

df.to_parquet("Log.parquet", index=False)
print("Saved Log.parquet")
