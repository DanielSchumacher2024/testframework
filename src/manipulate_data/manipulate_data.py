import pandas as pd
import numpy as np
import json
import random
import sys

detailed_logs = []
"""
Diese Funktion fuegt eine feste Anzahl von Duplikaten in den Datensatz ein.
Die Manipulation wird in einem globalen Logbuch festgehalten.
"""
def inject_duplicates(df, num_duplicates):
    global detailed_logs
    duplicates = df.sample(n=num_duplicates, replace=True)
    for idx, row in duplicates.iterrows():
        detailed_logs.append({
            "action": "duplicate",
            "id": row["id"],
            "column": None,
            "original_value": None,
            "new_value": None
        })
    return pd.concat([df, duplicates], ignore_index=True)

"""
Diese Funktion fuegt eine feste Anzahl von fehlenden Werten in den Datensatz ein.
Die Manipulation wird in einem globalen Logbuch festgehalten.
"""
def inject_missing_values(df, num_missing):
    global detailed_logs
    columns = [col for col in df.columns if col.lower() != "id"]
    total_possible = len(df) * len(columns)
    num_missing_fixed = min(num_missing, total_possible)
    possible_pairs = [(idx, col) for idx in df.index for col in columns]
    selected_pairs = random.sample(possible_pairs, num_missing_fixed)
    
    for idx, col in selected_pairs:
        original_value = df.at[idx, col]
        detailed_logs.append({
            "action": "missing",
            "id": df.at[idx, "id"],
            "column": col,
            "original_value": original_value,
            "new_value": None
        })
        df.at[idx, col] = np.nan
    return df

"""	
main definiert den Programmfluss.
Sie liest die Konfigurationsdatei ein und manipuliert die Daten entsprechend.
Der manipulierte Datensatz wird in einer Ausgabedatei gespeichert.
Die Protokoldatei wird in einer Ausgabedatei gespeichert.
"""
def main():
    try:
        with open("manipulate_config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        print("Konfigurationsdatei manipulate_config.json wurde nicht gefunden.")
        sys.exit(1)

    if "random_seed" in config:
        seed = config["random_seed"]
        np.random.seed(seed)
        random.seed(seed)

    input_file = config.get("input_file", "synthetic_data.csv")
    df = pd.read_csv(input_file)

    errors_list = config.get("errors", [])
    for error in errors_list:
        if not error.get("enabled", False):
            continue
        error_type = error.get("error_type")
        number = error.get("number")
        if error_type == "duplicates":
            df = inject_duplicates(df, number)
        elif error_type == "missing_values":
            df = inject_missing_values(df, number)
        else:
            sys.exit(1)

    output_file = config.get("output_file", "manipulated_data.csv")
    df.to_csv(output_file, index=False)

    if detailed_logs:
        detailed_log_df = pd.DataFrame(detailed_logs)
        detailed_log_file = config.get("protocol_file", "protocol_file.csv")
        detailed_log_df.to_csv(detailed_log_file, index=False)

if __name__ == "__main__":
    main()