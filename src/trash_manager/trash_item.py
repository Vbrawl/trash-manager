import datetime


class TrashItem:
    def __init__(self, original_path: str, deletion_date: str):
        self.original_path = ''
        self.deletion_date = datetime.datetime(1, 1, 1, 0, 0, 0)
