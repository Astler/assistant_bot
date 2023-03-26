
from data.config import A_PATH


def get_sa() -> list:
    from cat.utils.git_utils import get_json_data
    return get_json_data(A_PATH)

def is_sa(user_id: int) -> bool:
    return user_id in get_sa()