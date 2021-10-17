import json
import os


def get_user_file(user_id: int):
    return os.getcwd() + f"/users/{user_id}.json"


def get_user_dict(user_id: int):
    open(get_user_file(user_id), 'a').close()
    user_file = open(get_user_file(user_id), 'r')
    contents = user_file.read()
    user_file.close()

    if len(contents) != 0:
        user_data = json.loads(contents)
    else:
        user_data = {"delete_simple_command_requests": False}
        save_user_dict(user_id, user_data)

    print(user_data)

    return user_data


def save_user_dict(user_id: int, user_dict):
    with open(get_user_file(user_id), 'w') as f:
        f.write(json.dumps(user_dict))


def delete_simple_commands(user_id: int):
    return get_user_dict(user_id).get("delete_simple_command_requests", False)
