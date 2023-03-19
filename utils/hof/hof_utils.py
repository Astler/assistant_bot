import requests

from data.config import HOF_URL

class HOFItem:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def encode_hof(obj):
    if isinstance(obj, HOFItem):
        return {"mName": obj.name, "mDescription": obj.description}
    raise TypeError(repr(obj) + " is not JSON serializable")

def load_hof_array():
    try:
        response = requests.get(HOF_URL)
        response.raise_for_status()
        hof_json_array = response.json()
    except Exception as e:
        return f"Finished with error: {e}"

    return [HOFItem(item['mName'], item['mDescription']) for item in hof_json_array]