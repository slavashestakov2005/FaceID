from .database import Table, Row


class Face(Row):
    """
        Строка таблицы ListenersTable
        face    INT     NOT NULL    PK
    """
    fields = ['face']

    def __init__(self, row):
        Row.__init__(self, Face, row)


class FacesTable:
    table = "face"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(FacesTable.table, '''(
        "face"	INTEGER NOT NULL UNIQUE,
        PRIMARY KEY("face")
        )''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(FacesTable.table, Face)

    @staticmethod
    def exists(face: int) -> bool:
        return not Table.select_one(FacesTable.table, Face, 'face', face).__is_none__

    @staticmethod
    def insert(face: int) -> None:
        return Table.insert(FacesTable.table, Face([face]))

    @staticmethod
    def delete_face(face: int) -> None:
        return Table.delete(FacesTable.table, 'face', face)
