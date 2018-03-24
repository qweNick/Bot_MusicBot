# s__rock_song_id = "rock_song_id"
# s__band_id = "band_id"
# s__name = "name"
# s__title = "title"
# s__level_top = "level_top"
# s__level_down = "level_down"
# s__telegram_id = "telegram_id"
# s__source_url = "source_url"
# s__time = "time"


class song:
    def __init__(self, fields):
        self.__song_id = fields[0]
        self.__band_id = fields[1]
        self.__name = fields[2]
        self.__title = fields[3]
        self.__level_top = 0
        self.__level_down = 0
        self.__level_top_old = fields[4]
        self.__level_down_old = fields[5]
        self.__telegram_id = fields[6]
        self.__source_url = fields[7]
        self.__time = fields[8]
        self.__last_date = fields[9]

        self.__voted_users_id = []
        self.__message_telegram_id = -1

    def set_fields(self, fields):
        self.__song_id = fields[0]
        self.__band_id = fields[1]
        self.__name = fields[2]
        self.__title = fields[3]
        self.__level_top = fields[4]
        self.__level_down = fields[5]
        self.__telegram_id = fields[6]
        self.__source_url = fields[7]
        self.__time = fields[8]
        self.__last_date = fields[9]

    def get_song_id(self):
        return self.__song_id

    def get_band_id(self):
        return self.__band_id

    def get_name(self):
        return self.__name

    def get_title(self):
        return self.__title

    def get_level_top(self):
        return self.__level_top

    def get_level_down(self):
        return self.__level_down

    def get_telegram_id(self):
        return self.__telegram_id

    def get_source_url(self):
        return self.__source_url

    def get_time(self):
        return self.__time

    def get_last_date(self):
        return self.__last_date

    def set_last_date(self, last_date):
        self.__last_date = last_date

    def get_voted_users_id(self):
        return self.__voted_users_id

    def add_voted_user_id(self, user_id):
        self.__voted_users_id.append(user_id)

    def find_by_user_id(self, user_id):
        return user_id in self.__voted_users_id

    def append_voted_user_id(self, user_id):
        self.__voted_users_id.append(user_id)

    def rise_level_top(self, value=1):
        self.__level_top += value
        return self.__level_top

    def drop_level_top(self, value=1):
        self.__level_top -= value
        return self.__level_top

    def rise_level_down(self, value=1):
        self.__level_down += value
        return self.__level_down

    def drop_level_down(self, value=1):
        self.__level_down -= value
        return self.__level_down

    def get_message_telegram_id(self):
        return self.__message_telegram_id

    def set_message_telegram_id(self, message_id):
        self.__message_telegram_id = message_id

    def get_level_top_old(self):
        return self.__level_top_old

    def get_level_down_old(self):
        return self.__level_down_old




