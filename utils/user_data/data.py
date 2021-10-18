import json

from github import GithubException

from loader import repository


def get_user_file(user_id: int):
    return f"users/{user_id}.json"


def get_user_dict(user_id: int):
    try:
        file = repository.get_contents(get_user_file(user_id))
        print(file.decoded_content.decode())

        contents = file.decoded_content.decode()

        if len(contents) != 0:
            user_data = json.loads(contents)
        else:
            user_data = {"delete_simple_command_requests": False}
            save_user_dict(user_id, user_data)

    except GithubException:
        user_data = {"delete_simple_command_requests": False}
        save_user_dict(user_id, user_data)

    print(user_data)

    return user_data


def save_user_dict(user_id: int, user_dict):
    file_name = get_user_file(user_id)
    try:
        contents = repository.get_contents(file_name)
        repository.update_file(file_name, "user file", json.dumps(user_dict), contents.sha)
    except GithubException:
        repository.create_file(file_name, "user file", json.dumps(user_dict))


def delete_simple_commands(user_id: int):
    return get_user_dict(user_id).get("delete_simple_command_requests", False)
