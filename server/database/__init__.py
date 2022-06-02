from .database import *
from .face import *
from .listener import *
from ..config import Config


def create_tables():
    if Config.DROP_DB:
        FacesTable.create_table()
        ListenersTable.create_table()
