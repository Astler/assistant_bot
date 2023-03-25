from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import push_git_data, get_cached_git


class ChatToListenData(Serializable):
    chat_id = 0
    hashtag = ""

    def __init__(self, chat_id=0):
        self.chat_id = chat_id

    @staticmethod
    def from_json(json_dct: dict):
        info = ChatToListenData()

        info.chat_id = json_dct.get("chat_id", info.chat_id)
        info.hashtag = json_dct.get("hashtag", info.hashtag)

        return info


class ListenerData(Serializable):
    chats_to_listen = {}

    def to_json(self):
        chats = {}

        for char_id, chat_obj in self.chats_to_listen.items():
            chats[int(char_id)] = chat_obj.to_json_str()

        print(chats)

        json_dict = self.__dict__.copy()
        json_dict["chats_to_listen"] = chats

        return json_dict

    @staticmethod
    def from_json(json_dct: dict):
        info = ListenerData()

        raw_chats: dict = json_dct.get("chats_to_listen", info.chats_to_listen)
        print(raw_chats)
        chats_to_listen = {}

        for raw_chat_id, data in raw_chats.items():
            print(data)
            user = ChatToListenData.from_json_str(data)
            chats_to_listen[int(raw_chat_id)] = user

        info.chats_to_listen = chats_to_listen

        return info


def get_git_listener_data_file():
    return f"listener_data.json"


def get_listener_data() -> ListenerData:
    return get_cached_git(get_git_listener_data_file(), ListenerData())


def save_listener_data(data: ListenerData):
    file_name = get_git_listener_data_file()

    save_local_json(file_name, data)
    push_git_data(file_name, data)
