import json

from github import GithubException

from loader import repository


def get_group_file(group_id: int):
    return f"groups/{group_id}.json"


def get_group_dict(group_id: int):
    try:
        file = repository.get_contents(get_group_file(group_id))
        print(file.decoded_content.decode())

        contents = file.decoded_content.decode()

        if len(contents) != 0:
            user_data = json.loads(contents)
        else:
            user_data = {"blocked_links": []}
            save_group_dict(group_id, user_data)

    except GithubException:
        user_data = {"blocked_links": []}
        save_group_dict(group_id, user_data)

    print("get!")
    print(user_data)

    return user_data


def save_group_dict(user_id: int, user_dict):
    file_name = get_group_file(user_id)

    print(user_dict)

    try:
        contents = repository.get_contents(file_name)
        repository.update_file(file_name, "group file", json.dumps(user_dict), contents.sha)
    except GithubException:
        repository.create_file(file_name, "group file", json.dumps(user_dict))


def get_blocked_links(group_id: int):
    return get_group_dict(group_id).get("blocked_links", False)
