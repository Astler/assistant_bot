import json
import logging


def generate_json_string(item, default):
    logging.info("encode data")
    return json.JSONEncoder(default=default, sort_keys=True, indent=4 * ' ', ensure_ascii=False).encode(item)