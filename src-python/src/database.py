import os
import json
import settings

TAG_DEMO = {
    "id": "123",
    "label": "demo tag",
    "song": "test.mp3"
}

DATA_INITIAL = {
    "tags": [TAG_DEMO],
    "downloaded_songs": []
}

# Pre-populate data with defaults
data = DATA_INITIAL

# Load data from file
if os.path.isfile(settings.FN_DATABASE):
    with open(settings.FN_DATABASE) as f:
        data = json.loads(f.read())

# Write data to file
def _write_data_to_file():
    with open(settings.FN_DATABASE, "w") as f:
        f.write(json.dumps(data))

def get(key, defaultValue=None):
    """ Get a key, if not existing return defaultValue or None """
    return data[key] if key in data else defaultValue

def get_tag(rfid_id):
    for tag in data["tags"]:
        if tag["id"] == rfid_id:
            return tag
    return None

def add_tag(tag):
    # If tag already exists, remove it first
    _tag = get_tag(tag["id"])
    if _tag:
        data["tags"].remove(_tag)

    # Now add the new tag
    data["tags"].append(tag)
    _write_data_to_file()

def delete_tag(tagId):
    # If tag already exists, remove it first
    _tag = get_tag(tagId)
    if not _tag:
        return
    data["tags"].remove(_tag)
    _write_data_to_file()

def set(key, value):
    """ Set a key and save to file """
    data[key] = value
    _write_data_to_file()

if __name__ == "__main__":
    print(get("xxx"))
    set("xxx", 123)
    print(get("xxx"))

