from .database import Table, Row


class Listener(Row):
    """
        Строка таблицы ListenersTable
        face    INT     NOT NULL    PK
        chat    INT     NOT NULL    PK
    """
    fields = ['face', 'chat']

    def __init__(self, row):
        Row.__init__(self, Listener, row)


class ListenersTable:
    table = "listeners"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(ListenersTable.table, '''(
        "face"	INTEGER NOT NULL,
        "chat"	INTEGER NOT NULL,
        PRIMARY KEY("face","chat")
        )''')
        ListenersTable.insert(Listener([-1, 1095985234]))

    @staticmethod
    def select_all() -> list:
        return Table.select_list(ListenersTable.table, Listener)

    @staticmethod
    def select_by_face(face: int) -> list:
        listeners = Table.select_list(ListenersTable.table, Listener, 'face', face)
        listeners.extend(Table.select_list(ListenersTable.table, Listener, 'face', -1))
        return listeners

    @staticmethod
    def exists(listener: Listener) -> bool:
        return not Table.select_one(ListenersTable.table, Listener, 'face', listener.face, 'chat', listener.chat).__is_none__

    @staticmethod
    def insert(listener: Listener) -> None:
        return Table.insert(ListenersTable.table, listener)

    @staticmethod
    def delete_face(face: int) -> None:
        return Table.delete(ListenersTable.table, 'face', face)

    @staticmethod
    def delete(listener: Listener) -> None:
        return Table.delete(ListenersTable.table, 'face', listener.face, 'chat', listener.chat)
