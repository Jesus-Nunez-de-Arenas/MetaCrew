import os
import json

input_folder = "output_mmmu/"
output_file = "merged_answers.jsonl"
merged_data = []

for filename in os.listdir(input_folder):
    if filename.endswith(".jsonl"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                # Extract required fields if they exist
                entry = {
                    "id": data.get("id"),
                    "options": data.get("options"),
                    "golden_answer": data.get("correct_answer"),
                    "final_answer": data.get("final_prediction")
                }
                merged_data.append(entry)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)