import sys
import json
import csv
import random
import string
from datetime import datetime, timedelta

"""
Diese Funktion generiert zufaellige Werte fuer den Datentyp int.
value_range ist eine Liste mit zwei Elementen, die den Wertebereich fuer die Zufallswerte angibt.
Ist value_range nicht angegeben (also false), wird ein zufaelliger Wert zwischen 0 und 100 generiert.
"""
def random_int(value_range=None):
    if value_range and isinstance(value_range, list) and len(value_range) == 2:
        return random.randint(value_range[0], value_range[1])
    else:
        return random.randint(0, 100)
    
"""
Diese Funktion generiert zufaellige Werte fuer den Datentyp string.
value_range ist eine Liste mit moeglichen Werten, aus denen zufaellig ausgewaehlt wird.
Ist value_range nicht angegeben (also false), wird ein zufaelliger Name aus einer Liste von Standardnamen gewaehlt.
"""
def random_string(value_range=None):
    if value_range and isinstance(value_range, list):
        return random.choice(value_range)
    else:
        default_names = ["Alice", "Bob", "Charlie", "Diana"]
        return random.choice(default_names)

""""
Diese Funktion generiert zufaellige Werte fuer den Datentyp boolean.
value_range ist eine Liste mit den moeglichen Werten, die der booleanen Variable annehmen kann.
Ist value_range nicht angegeben (also false), wird zufaellig True oder False zurueckgegeben.
"""  
def random_boolean(value_range=None):
    if value_range and isinstance(value_range, list):
        return random.choice(value_range)
    else:
        return random.choice([True, False])

""""
generate_value ist die Hauptfunktion, die je nach Datentyp und Wertebereich den geforderten Wert generiert und zurueckgibt."
data_type ist der Datentyp des Wertes, der generiert werden soll.
value_range ist der Wertebereich, aus dem der Wert generiert werden soll (falls zutreffend).
"""
def generate_value(data_type, value_range):
    if not data_type:
        print("Problem: Kein Datentyp angegeben. Bitte geben Sie einen unterstuetzten Datentyp an.")
        sys.exit(1)
    data_type = data_type.lower()
    if data_type == "int":
        return random_int(value_range)
    elif data_type == "string":
        return random_string(value_range)
    elif data_type == "boolean":
        return random_boolean(value_range)
    else:
        print(f"Problem: Unbekannter Datentyp {data_type}. Bitte verwenden Sie einen unterstuetzten Datentyp.")
        sys.exit(1)

"""
main defniert den Programmfluss.
Sie liest Konfigurationsdatei ein und generiert die synthetischen Daten."
Wenn keine ID-Spalte in der Konfiguration angegeben ist, wird automatisch eine fortlaufende ID-Spalte hinzugefuegt.
Wird kein Name fuer die Ausgabedatei angegeben, wird standardmaeßig synthetic_data.csv verwendet.
"""
def main():
    try:
        with open("gen_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Problem: Die Konfigurationsdatei config.json wurde nicht gefunden.")
        sys.exit(1)

    num_rows = config.get("rows", 100)
    output_file = config.get("output_file", "synthetic_data.csv")
    columns = config.get("columns", [])

    header = []
    col_defs = []
    for col in columns:
        name = col.get("name", "col")
        data_type = col.get("type")
        value_range = col.get("range", None)
        header.append(name)
        col_defs.append((data_type, value_range))
    
    if not any(name.lower() == "id" for name in header):
        header.insert(0, "id")
        col_defs.insert(0, ("sequential", None))

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in range(num_rows):
            row = []
            for dt, vr in col_defs:
                if dt.lower() == "sequential":
                    row.append(i + 1)
                else:
                    row.append(generate_value(dt, vr))
            writer.writerow(row)

    print(f"Datensatz mit {num_rows} Zeilen und {len(header)} Spalten wurde in {output_file} gespeichert.")

if __name__ == "__main__":
    main()