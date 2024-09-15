from __future__ import annotations
import datetime
import platform
from pathlib import Path


class ITrashItem:
    def __init__(self, original_path: str, deletion_date: datetime.datetime):
        self.original_path = original_path
        self.deletion_date = deletion_date


if platform.system() == "Linux":
    class TrashItem(ITrashItem):
        def __init__(self, original_path: str, deletion_date: datetime.datetime, trashed_path: str, trashinfo_path: str):
            ITrashItem.__init__(self, original_path, deletion_date)
            self.trashed_path = trashed_path
            self.trashinfo_path = trashinfo_path

        @staticmethod
        def for_trashed_file(path: str) -> TrashItem:
            def find_tag(start: int, tag: str):
                pos = content.find(tag, start)
                if pos == -1:
                    return -1, 0
                end_pos = content.find(b'\n', pos)
                if end_pos == -1:
                    return -1, 0
                return pos + len(tag), end_pos

            trash_info_tag = b"[Trash Info]"
            path_tag = b"Path="
            deletion_date_tag = b"DeletionDate="

            path = Path(path)
            trashinfo_path = path.parent.parent / "info" / (path.name + ".trashinfo")
            with open(str(trashinfo_path), 'rb') as f:
                content = f.read()

            trash_info_pos = content.find(trash_info_tag)
            if trash_info_pos == -1:
                return None

            path_pos, path_end_pos = find_tag(trash_info_pos, path_tag)
            if path_pos == -1:
                return None

            deletion_date_pos, deletion_date_end_pos = find_tag(trash_info_pos, deletion_date_tag)
            if deletion_date_pos == -1:
                return None

            path_value = content[path_pos:path_end_pos].decode()
            deletion_date_value = datetime.datetime.fromisoformat(content[deletion_date_pos:deletion_date_end_pos].decode())
            return TrashItem(path_value, deletion_date_value, str(path), str(trashinfo_path))
