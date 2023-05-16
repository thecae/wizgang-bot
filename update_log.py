import json
import sys


# get the current changelog
def load_changelog():
    with open('storage/changelog.json', 'r') as f:
        return json.load(f)


def save_changelog(log):
    with open('storage/changelog.json', 'w') as f:
        json.dump(log, f, indent=4)


version, date = sys.argv[1], sys.argv[2]
changelog = load_changelog()
changelog.append({'version': version, 'date': date})
save_changelog(changelog)
print("Changelog updated.")
