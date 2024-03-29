import json

from github import GithubException

from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_file, save_local_json
from cat.utils.telegram_utils import send_telegram_msg_to_me
from loader import repository


def push_git_serializable_data(file_path: str, serializable: Serializable):
    json_str = serializable.to_json_str()
    push_git_str_data(file_path, json_str)


def push_git_str_data(file_path: str, data: str):
    try:
        contents = repository.get_contents(file_path)
        repository.update_file(file_path, f"info: {file_path}", data, contents.sha)
    except GithubException:
        repository.create_file(file_path, f"info: {file_path}", data)


def get_json_data(path_to_file: str, fallback_data=None):
    try:
        file = repository.get_contents(path_to_file)
        contents = file.decoded_content.decode()
        cer = json.loads(contents)
    except GithubException:
        if fallback_data is not None:
            cer = fallback_data
        else:
            cer = {}

    return cer


def get_serializable_git(path_to_file: str, fallback_data: Serializable):
    data = fallback_data

    try:
        file = repository.get_contents(path_to_file)
        contents = file.decoded_content.decode()

        if len(contents) != 0:
            data = data.from_json_str(contents)

    except GithubException as exception:
        send_telegram_msg_to_me(f"Exception: {exception} {path_to_file}")
        push_git_serializable_data(path_to_file, data)

    save_local_json(path_to_file, data)

    return data
