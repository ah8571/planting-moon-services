import json

# Load the directories data
with open('data/directories.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Track changes
updated_count = 0
directories_updated = []

# Update all directories from submitatool.com to have free submission type
for directory in data['directories']:
    if 'listedOn' in directory and 'submitatool.com' in directory['listedOn']:
        if directory.get('submissionType') == 'unknown':
            directory['submissionType'] = 'free'
            updated_count += 1
            directories_updated.append(directory.get('name', 'Unknown'))

# Save the updated data
with open('data/directories.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {updated_count} directories from submitatool.com to 'free' submission type")
print("\nUpdated directories:")
for name in sorted(directories_updated):
    print(f"  - {name}")
