from db_sqlite.db_structure.tables.rock_songs import rock_songs
from db_sqlite.db_structure.tables.rock_bands import rock_bands
#from db_sqlite.db_structure.tables.history_of_sending_songs import history_of_sending_songs
from db_sqlite.db_structure.tables.users import users


class db:
    rock_bands = rock_bands()
    rock_songs = rock_songs()
    #history_of_sending_songs = history_of_sending_songs()
    users = users()
