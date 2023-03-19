def save_file(path_to_file: str, data: str):
    f = open(path_to_file, "w", encoding='utf-8')
    f.write(data)
    f.close()