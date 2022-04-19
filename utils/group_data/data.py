import json
import os

from github import GithubException

from loader import repository
from utils.group_data.group_info import GroupInfo


def get_group_dict(group_id: int) -> GroupInfo:
    if os.path.exists(get_local_file(group_id)):
        try:
            return get_local_dict(group_id)
        except Exception as e:
            print(e)
            return get_git_dict(group_id)
    else:
        return get_git_dict(group_id)


def save_group_dict(group_id: int, group_info: GroupInfo):
    file_name = get_git_group_file(group_id)

    try:
        contents = repository.get_contents(file_name)
        repository.update_file(file_name, "group file", json.dumps(group_info.to_json()), contents.sha)
    except GithubException:
        repository.create_file(file_name, "group file", json.dumps(group_info.to_json()))

    save_local_dict(group_id, group_info)


def get_blocked_links(group_id: int):
    return get_group_dict(group_id).blocked_links


def get_delete_commands(group_id: int):
    return get_group_dict(group_id).delete_commands


def get_last_settings_msg(group_id: int):
    return get_group_dict(group_id).last_settings_msg_id


### LOCAL ###

def get_local_file(group_id: int):
    return os.getcwd() + f"/groups/{group_id}.json"


def get_local_dict(group_id: int):
    open(get_local_file(group_id), 'a').close()
    user_file = open(get_local_file(group_id), 'r')
    contents = user_file.read()
    user_file.close()

    if len(contents) != 0:
        group_data = json.loads(contents)
        return GroupInfo.from_json(group_data)
    else:
        empty_data = GroupInfo()
        save_local_dict(group_id, empty_data)
        return empty_data


def save_local_dict(group_id: int, group_info: GroupInfo):
    filename = get_local_file(group_id)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            print(exc)

    with open(filename, 'w') as f:
        f.write(json.dumps(group_info.to_json()))


### GITHUB ###

def get_git_group_file(group_id: int):
    return f"groups/{group_id}.json"


def get_git_dict(group_id: int) -> GroupInfo:
    try:
        file = repository.get_contents(get_git_group_file(group_id))

        contents = file.decoded_content.decode()

        if len(contents) != 0:
            group_info = GroupInfo.from_json(json.loads(contents))
        else:
            group_info = GroupInfo()
            save_local_dict(group_id, group_info)

    except GithubException:
        user_data = {"blocked_links": [], "delete_commands": True, "last_settings_msg_id": 0}
        save_group_dict(group_id, group_info)

    print("GIT LOADED!")

    save_local_dict(group_id, group_info)

    return group_info
