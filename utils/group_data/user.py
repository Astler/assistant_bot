import json
from json import JSONEncoder


class CatUser:
    user_id = 0
    reputation = 0

    def __init__(self, user_id=0, reputation=0):
        self.user_id = user_id
        self.reputation = reputation

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    class CatUserEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
