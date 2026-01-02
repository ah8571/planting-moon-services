import json
import csv
import glob
import os

# Get review directories from CSV
csv_reviews = set()
csv_file = glob.glob('data/*.csv')[0]
print(f"Found CSV: {csv_file}")

with open(csv_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig removes BOM
    reader = csv.DictReader(f)
    print(f"CSV Headers: {reader.fieldnames}")
    for row in reader:
        if row and row.get('Type') and 'Review Directory' in row['Type']:
            csv_reviews.add(row['Name'].strip())

print(f"Total Review Directories in CSV: {len(csv_reviews)}")
print(f"Sample review directories: {sorted(list(csv_reviews))[:5]}")

# Get from JSON and check if they have 'type' field captured
directories = json.load(open('data/directories.json'))['directories']
json_with_type = {}
missing_from_json = []

for dir_entry in directories:
    name = dir_entry.get('name', '')
    type_field = dir_entry.get('type', '')
    if name in csv_reviews:
        json_with_type[name] = type_field

for csv_name in csv_reviews:
    if csv_name not in json_with_type:
        missing_from_json.append(csv_name)

print(f"\nReview directories found in JSON: {len(json_with_type)}")
print(f"Missing from JSON: {len(missing_from_json)}")

if missing_from_json:
    print(f"Missing entries: {missing_from_json}")

# Show entries that have type captured
with_type = {k: v for k, v in json_with_type.items() if v}
print(f"\nWith 'type' field captured: {len(with_type)}")
if with_type:
    print(f"Examples with type: {list(with_type.items())[:5]}")

without_type = {k: v for k, v in json_with_type.items() if not v}
print(f"Without 'type' field (empty): {len(without_type)}")
if without_type:
    print(f"Examples without type: {list(without_type.keys())[:5]}")
