import ftplib

from data.config import FTP_URL, FTP_USER, FTP_PASS


def upload_file_to_folder(path_to_file: str, folder: str = "apps_data"):
    file = open(path_to_file, 'rb')

    with ftplib.FTP(FTP_URL, FTP_USER, FTP_PASS) as ftp, file:
        ftp.storbinary(f'STOR /astler.net/{folder}/{file.name}', file)