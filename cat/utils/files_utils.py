import os

from cat.json.serializable import Serializable


def build_path(path_to_file: str):
    return os.getcwd() + "/" + path_to_file


def save_local_json(file_path: str, serializable: Serializable):
    save_local_file(file_path, serializable.to_json_str())


def save_local_file(file_path: str, file_data: str):
    file_path = build_path(file_path)

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            print(exc)

    with open(file_path, 'w') as f:
        f.write(file_data)
        print(f"write {file_data}")
