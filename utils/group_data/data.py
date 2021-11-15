import json
import os

from github import GithubException

from loader import repository


def get_group_dict(group_id: int):
    try:
        return get_local_dict(group_id)
    except Exception as e:
        print(e)
        return get_git_dict(group_id)


def save_group_dict(group_id: int, group_dict):
    file_name = get_git_group_file(group_id)

    try:
        contents = repository.get_contents(file_name)
        repository.update_file(file_name, "group file", json.dumps(group_dict), contents.sha)
    except GithubException:
        repository.create_file(file_name, "group file", json.dumps(group_dict))

    save_local_dict(group_id, group_dict)


def get_blocked_links(group_id: int):
    return get_group_dict(group_id).get("blocked_links", False)


def get_delete_commands(group_id: int):
    return get_group_dict(group_id).get("delete_commands", True)


def get_last_settings_msg(group_id: int):
    return get_group_dict(group_id).get("last_settings_msg_id", 0)


### LOCAL ###

def get_local_file(group_id: int):
    return os.getcwd() + f"\\groups\\{group_id}.json"


def get_local_dict(group_id: int):
    open(get_local_file(group_id), 'a').close()
    user_file = open(get_local_file(group_id), 'r')
    contents = user_file.read()
    user_file.close()

    if len(contents) != 0:
        group_data = json.loads(contents)
    else:
        group_data = {"blocked_links": [], "delete_commands": True}
        save_local_dict(group_id, group_data)

    print("LOCAL LOADED!")

    return group_data


def save_local_dict(group_id: int, group_dict):
    filename = get_local_file(group_id)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            print(exc)

    with open(filename, 'w') as f:
        f.write(json.dumps(group_dict))


### GITHUB ###

def get_git_group_file(group_id: int):
    return f"groups/{group_id}.json"


def get_git_dict(group_id: int):
    try:
        file = repository.get_contents(get_git_group_file(group_id))

        contents = file.decoded_content.decode()

        if len(contents) != 0:
            user_data = json.loads(contents)
        else:
            user_data = {"blocked_links": []}
            save_group_dict(group_id, user_data)

    except GithubException:
        user_data = {"blocked_links": [], "delete_commands": True, "last_settings_msg_id": 0}
        save_group_dict(group_id, user_data)

    print("GIT LOADED!")
    save_local_dict(group_id, user_data)

    return user_data
