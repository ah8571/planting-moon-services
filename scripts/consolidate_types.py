import json

# Load the JSON file
with open('data/directories.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define the type mappings
type_mappings = {
    "#1 website for AI tools worldwide": None,
    "Community": None,
    "International": None,
    "Media": None,
    "Others": None,
    "Developer Tools": "SaaS Directory",
    "Directory": "SaaS Directory",
    "General Directory": "SaaS Directory",
    "SaaS Marketplace": "SaaS Directory",
    "Software Directory": "SaaS Directory",
    "Startup Directory": "SaaS Directory",
    "Launchpad": "Launch Platform"
}

# Apply mappings to all entries
count_changes = {}
for directory in data["directories"]:
    old_type = directory.get("type")
    if old_type in type_mappings:
        new_type = type_mappings[old_type]
        directory["type"] = new_type
        key = f"{old_type} → {new_type}"
        count_changes[key] = count_changes.get(key, 0) + 1

# Save the updated JSON file
with open('data/directories.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Type consolidation complete!")
print("\nChanges made:")
for change, count in sorted(count_changes.items()):
    print(f"  {change}: {count} entries")

# Print summary of unique types now in the file
unique_types = {}
for directory in data["directories"]:
    dtype = directory.get("type")
    unique_types[dtype] = unique_types.get(dtype, 0) + 1

print("\nFinal type distribution:")
for dtype in sorted(unique_types.keys(), key=lambda x: (x is None, x)):
    print(f"  {dtype if dtype else 'null'}: {unique_types[dtype]}")
