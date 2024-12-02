import json
import pandas as pd

def excel_to_json(excel_file, json_file):
    df = pd.read_excel(excel_file)

    data = []
    for _, row in df.iterrows():
        data.append({
            "input": row["INPUT"],
            "output": row["OUTPUT"],
            "parameter": row["PARAMETER"],
            "solution": row["SOLUTION"]
        })

    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

excel_to_json("data\\manual_test.xlsx", "manual_test.json")