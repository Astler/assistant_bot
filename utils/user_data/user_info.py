class UserInfo:
    delete_simple_command_requests = True
    adult_mode = False
    pidor_times = 0
    hero_times = 0
    global_rating = 0
    user_admin_channels = []

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_dct: dict):
        info = UserInfo()

        info.delete_simple_command_requests = json_dct.get("delete_simple_command_requests",
                                                           info.delete_simple_command_requests)
        info.adult_mode = json_dct.get("adult_mode", info.adult_mode)
        info.pidor_times = json_dct.get("pidor_times", info.pidor_times)
        info.hero_times = json_dct.get("hero_times", info.hero_times)
        info.global_rating = json_dct.get("global_rating", info.global_rating)
        info.user_admin_channels = json_dct.get("user_admin_channels", info.user_admin_channels)

        return info
