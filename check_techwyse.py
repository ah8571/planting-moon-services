import json
data = json.load(open('data/guest-posts.json'))
for e in data['guestPosts']:
    if e['name'] == 'TechWyse':
        print(f"Name: {e['name']}")
        print(f"listedOn: {e['listedOn']}")
        break
