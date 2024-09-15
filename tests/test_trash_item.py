from pytest import fixture
from trash_manager import TrashItem
import datetime
from pathlib import Path


class FormattedData:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        s = "[Trash Info]\n"
        for k, v in self.__dict__.items():
            s += k
            s += '='
            s += v
            s += '\n'
        return s


@fixture
def trashinfo_data() -> FormattedData:
    return FormattedData(Path="/random/path", DeletionDate="2024-08-07T01:55:05")


def test_TrashItem__parse(trashinfo_data: FormattedData):
    fake_content = str(trashinfo_data).encode()
    titem = TrashItem("/trash/files/path", "/trash/info/path")
    titem._parse(fake_content)

    assert titem.original_path == trashinfo_data.Path
    assert titem.deletion_date == datetime.datetime.fromisoformat(trashinfo_data.DeletionDate)


def test_TrashItem_parse(tmp_path: Path, trashinfo_data: FormattedData):
    toparse = tmp_path / "parse_test.trashinfo"
    with open(toparse, "w") as f:
        f.write(str(trashinfo_data))

    titem = TrashItem("/trash/files/path", toparse)
    assert titem.original_path == trashinfo_data.Path
    assert titem.deletion_date == datetime.datetime.fromisoformat(trashinfo_data.DeletionDate)
