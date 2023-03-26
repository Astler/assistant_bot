import csv

from cat.utils.git_utils import push_git_str_data

advertisement = "Advertisement"
not_advertisement = "Not Advertisement"

label_names = [advertisement, not_advertisement]


async def add_new_data_to_ads_model(text: str, label: str):
    with open("labeled_messages.csv", mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([text, label])

    with open("labeled_messages.csv", mode="r", encoding="utf-8", newline="") as f:
        push_git_str_data("labeled_messages.csv", f.read())
