import json
import os

from github import GithubException

from loader import repository
from utils.user_data.user_info import UserInfo


def get_cached_user_file(user_id: int):
    return f"users/{user_id}.json"


def get_user_info(user_id: int) -> UserInfo:
    if os.path.exists(get_cached_user_file(user_id)):
        try:
            return get_local_user_info(user_id)
        except Exception as e:
            print(e)
            return get_git_user_info(user_id)
    else:
        return get_git_user_info(user_id)


def save_user_info(user_id: int, user_dict):
    file_name = get_cached_user_file(user_id)

    try:
        contents = repository.get_contents(file_name)
        repository.update_file(file_name, "user file", json.dumps(user_dict.to_json()), contents.sha)
    except GithubException:
        repository.create_file(file_name, "user file", json.dumps(user_dict.to_json()))

    save_local_user_info(user_id, user_dict)


def delete_simple_commands(user_id: int):
    return get_user_info(user_id).delete_simple_command_requests


def add_user_channel(user_id: int, channel_id: int):
    user_dict = get_user_info(user_id)
    data = user_dict.user_admin_channels

    if not data.__contains__(channel_id):
        data.append(channel_id)

    user_dict.user_admin_channels = data

    save_user_info(user_id, user_dict)


def get_user_channels(user_id: int):
    user_dict = get_user_info(user_id)
    return user_dict.user_admin_channels


### LOCAL ###

def get_local_user_info(user_id: int) -> UserInfo:
    open(get_cached_user_file(user_id), 'a').close()
    user_file = open(get_cached_user_file(user_id), 'r')
    contents = user_file.read()
    user_file.close()

    if len(contents) != 0:
        group_data = json.loads(contents)
        return UserInfo.from_json(group_data)
    else:
        empty_data = UserInfo()
        save_user_info(user_id, empty_data)
        return empty_data


def save_local_user_info(group_id: int, user_info: UserInfo):
    filename = get_cached_user_file(group_id)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            print(exc)

    with open(filename, 'w') as f:
        f.write(json.dumps(user_info.to_json()))


### GITHUB ###

def get_git_user_file(group_id: int):
    return f"users/{group_id}.json"


def get_git_user_info(group_id: int) -> UserInfo:
    user_info = UserInfo()

    try:
        file = repository.get_contents(get_git_user_file(group_id))

        contents = file.decoded_content.decode()

        if len(contents) != 0:
            user_info = UserInfo.from_json(json.loads(contents))
        else:
            save_user_info(group_id, user_info)

    except GithubException:
        save_user_info(group_id, user_info)

    save_local_user_info(group_id, user_info)

    return user_info
