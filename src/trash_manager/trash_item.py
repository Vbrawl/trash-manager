import datetime
import platform


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
