import pandas as pd
import os
import sys

REFERENCE_CSV = r"C:\Users\Pieter\Documents\AGI-26. San Francisco\tiled-world.csv"
LOG_PATH = "Log.parquet"


def load_reference():
    df = pd.read_csv(REFERENCE_CSV, sep=";", dtype=str, keep_default_na=False)
    # Build clusters: sentence -> list of rows
    clusters = {}
    current_key = None
    current_rows = []

    for _, row in df.iterrows():
        sentence = row["natural language input"].strip()
        is_separator = all(v == "" for v in row.values)

        if is_separator:
            if current_key is not None:
                clusters[current_key] = current_rows
                current_key = None
                current_rows = []
        elif sentence != "":
            if current_key is not None:
                clusters[current_key] = current_rows
            current_key = sentence.lower()
            current_rows = [row.to_dict()]
        else:
            # continuation row
            if current_key is not None:
                current_rows.append(row.to_dict())

    if current_key is not None:
        clusters[current_key] = current_rows

    return clusters


def load_log():
    if os.path.exists(LOG_PATH):
        return pd.read_parquet(LOG_PATH)
    cols = ["natural language input", "e0", "e1", "e2", "e3", "e4", "v", "threshold", "message output"]
    return pd.DataFrame(columns=cols).astype(str)


def insert_sentence(sentence, clusters, log_df):
    key = sentence.strip().lower()
    rows = clusters.get(key)

    if rows is None:
        print(f"[no match found for: '{sentence}']")
        return log_df

    new_rows = pd.DataFrame(rows)
    log_df = pd.concat([log_df, new_rows], ignore_index=True)
    log_df.to_parquet(LOG_PATH, index=False)

    for row in rows:
        msg = row.get("message output", "").strip()
        if msg:
            print(f">> {msg}")

    return log_df


def main():
    clusters = load_reference()
    log_df = load_log()

    if len(sys.argv) > 1:
        sentence = " ".join(sys.argv[1:])
        insert_sentence(sentence, clusters, log_df)
    else:
        print("Enter sentences (Ctrl+C to quit):")
        while True:
            try:
                sentence = input("> ").strip()
                if sentence:
                    log_df = insert_sentence(sentence, clusters, log_df)
            except (KeyboardInterrupt, EOFError):
                print()
                break


if __name__ == "__main__":
    main()
