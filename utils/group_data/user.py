import json
from json import JSONEncoder


class CatUser:
    user_id = 0
    reputation = 0
    last_edit_time = 0
    pidor_times = 0
    hero_times = 0

    def __init__(self, user_id=0, reputation=0, last_rep_edit_time=0, pidor_times=0):
        self.user_id = user_id
        self.reputation = reputation
        self.last_rep_edit_time = last_rep_edit_time
        self.pidor_times = pidor_times

    def increment_hero_counter(self):
        self.hero_times += 1
        return self

    def increment_pidor_counter(self):
        self.pidor_times += 1
        return self

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    class CatUserEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
