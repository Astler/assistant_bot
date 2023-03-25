from github import GithubException

from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_file, save_local_json
from loader import repository


def push_git_data(file_path: str, serializable: Serializable):
    json_str = serializable.to_json_str()

    try:
        contents = repository.get_contents(file_path)
        repository.update_file(file_path, f"info: {file_path}", json_str, contents.sha)
    except GithubException:
        repository.create_file(file_path, f"info: {file_path}", json_str)


def push_git_data(file_path: str, data: str):
    try:
        contents = repository.get_contents(file_path)
        repository.update_file(file_path, f"info: {file_path}", data, contents.sha)
    except GithubException:
        repository.create_file(file_path, f"info: {file_path}", data)


def get_cached_git(path_to_file: str, fallback_data: Serializable):
    data = fallback_data

    try:
        file = repository.get_contents(path_to_file)
        contents = file.decoded_content.decode()

        if len(contents) != 0:
            data = data.from_json_str(contents)

    except GithubException:
        push_git_data(path_to_file, data)

    save_local_json(path_to_file, data)

    return data
