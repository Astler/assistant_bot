import json

from github import GithubException

from data.config import CERT_PATH, A_PATH
from loader import repository


def get_cer_data():
    try:
        file = repository.get_contents(CERT_PATH)
        contents = file.decoded_content.decode()
        cer = json.loads(contents)
    except GithubException:
        cer = {}

    return cer


def get_a_list():
    try:
        file = repository.get_contents(A_PATH)
        contents = file.decoded_content.decode()
        a = json.loads(contents)
    except GithubException:
        a = []

    return a
