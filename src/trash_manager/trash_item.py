from typing import Optional
import datetime
from pathlib import Path


class TrashItem:
    def __init__(self, trash_path: str, trash_info_path: str):
        self.trash_path = Path(trash_path)
        self.trash_info_path = Path(trash_info_path)

        self.original_path = ''
        self.deletion_date = datetime.datetime(1, 1, 1, 0, 0, 0)

        if self.trash_info_path.exists():
            self.parse()

    def _parse(self, contents: bytes):
        trash_tag = b"[Trash Info]"
        path_tag = b"Path="
        deletion_date_tag = b"DeletionDate="

        trash_info = contents.find(trash_tag)
        if trash_info == -1:
            return

        trash_info += len(trash_tag)
        path_info = contents.find(path_tag, trash_info)
        deletion_date_info = contents.find(deletion_date_tag, trash_info)

        self.original_path = contents[path_info:].split(b'=', 1)[-1].split(b'\n')[0].decode()
        deletion_date_data = contents[deletion_date_info:].split(b'=', 1)[-1].split(b'\n')[0].decode()
        self.deletion_date = datetime.datetime.fromisoformat(deletion_date_data)

    def parse(self):
        with open(self.trash_info_path, 'rb') as infofile:
            contents = infofile.read()
        self._parse(contents)

    def isvalid(self) -> bool:
        return self.trash_path.exists() and self.trash_info_path.exists()
