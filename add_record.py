import pandas as pd
import os

LOG_PATH = "Log.parquet"

COLUMNS = ["natural language input", "e0", "e1", "e2", "e3", "e4", "v", "threshold", "message output"]


def load_log():
    if os.path.exists(LOG_PATH):
        return pd.read_parquet(LOG_PATH)
    return pd.DataFrame(columns=COLUMNS).astype(str)


def main():
    log_df = load_log()
    record = {}

    print("Enter values for each column (press Enter to leave blank):")
    for col in COLUMNS:
        value = input(f"  {col}: ").strip()
        record[col] = value

    new_row = pd.DataFrame([record])
    log_df = pd.concat([log_df, new_row], ignore_index=True)
    log_df.to_parquet(LOG_PATH, index=False)

    print("Record added to Log.parquet.")


if __name__ == "__main__":
    main()
