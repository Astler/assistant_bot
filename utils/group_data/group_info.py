class GroupInfo:
    hero_name = "Красавчик"
    additional_hero_name = "Овощ"
    blocked_links = []
    delete_commands = True
    last_settings_msg_id = 0
    users = {}
    pidors = {}
    heroes = {}
    adult_mode = False

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_dct: dict):
        info = GroupInfo()

        info.hero_name = json_dct.get("hero_name", info.hero_name)
        info.additional_hero_name = json_dct.get("additional_hero_name", info.additional_hero_name)
        info.blocked_links = json_dct.get("blocked_links", info.blocked_links)
        info.delete_commands = json_dct.get("delete_commands", info.delete_commands)
        info.last_settings_msg_id = json_dct.get("last_settings_msg_id", info.last_settings_msg_id)
        info.users = json_dct.get("users", info.users)
        info.heroes = json_dct.get("heroes", info.heroes)
        info.adult_mode = json_dct.get("adult_mode", info.adult_mode)

        return info
