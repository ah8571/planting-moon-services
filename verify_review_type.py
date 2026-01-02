import json
from collections import Counter

# Load directories
dirs = json.load(open('data/directories.json'))['directories']

# Count entries by submissionType
submission_types = Counter()
for d in dirs:
    submission_type = d.get('submissionType', 'unknown')
    submission_types[submission_type] += 1

print("Submission types in directories.json:")
for subtype, count in sorted(submission_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {subtype}: {count}")

# Look for review directories
print("\n\nReview directory entries:")
review_dirs = [d for d in dirs if d.get('submissionType') == 'review']
print(f"Total review directories: {len(review_dirs)}\n")
if review_dirs:
    print("Review directories found:")
    for d in review_dirs:
        print(f"  - {d['name']}")
else:
    print("WARNING: No review directories found in directories.json!")
    print("\nAvailable submission types:")
    for d in dirs[:5]:
        print(f"  {d['name']}: {d.get('submissionType', 'N/A')}")
