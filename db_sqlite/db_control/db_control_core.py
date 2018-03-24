from db_sqlite.db_structure.db import db
from db_sqlite.basic_commands import db_sqlite_basic_commands as db_sql


class db_control_core:
    db = db()

    def __init__(self):
        self.__bands = self.__get_all_bands()
        self.__songs = self.__get_all_songs()
        self.__users = self.__get_all_users()

    def __get_all_bands(self):
        cn = [self.db.rock_bands.s__rock_band_id, self.db.rock_bands.s__group_name, self.db.rock_bands.s__group_title,
              self.db.rock_bands.s__level_top,
              self.db.rock_bands.s__level_down, self.db.rock_bands.s__country]
        return db_sql.select_cn_from_t1(self.db.rock_bands.table_name, cn)

    def __update_all_bands(self):
        self.__bands = self.__get_all_bands()

    def __find_all_bands(self, band):
        for _band in self.__bands:
            if _band[1] == band:
                return _band
        return False

    def __add_rock_song(self, band_id, name, title, url, time=False):
        # s__rock_song_id = "rock_song_id"
        # s__band_id = "band_id"
        # s__name = "name"
        # s__title = "title"
        # s__level = "level"
        # s__telegram_id = "telegram_id"
        # s__source_url = "source_url"
        pn = [self.db.rock_songs.s__band_id, self.db.rock_songs.s__name, self.db.rock_songs.s__title,
              self.db.rock_songs.s__source_url]
        vn = [band_id, name, title, url]
        if time:
            pn.append(self.db.rock_songs.s__time)
            vn.append(time)
        db_sql.insert_into_t1_pn_values_vn(self.db.rock_songs.table_name, pn, vn)

    def __add_rock_band(self, band, title):
        # s__rock_band_id = "rock_band_id"
        # s__group_name = "group_name"
        # s__level = "level"
        # s__country = "country"
        pn = [self.db.rock_bands.s__group_name, self.db.rock_bands.s__group_title]
        vn = [band, title]
        # if country:
        #     pn.append(self.db.rock_bands.s__country)
        #     vn.append(country)
        db_sql.insert_into_t1_pn_values_vn(self.db.rock_bands.table_name, pn, vn)

    def __correct_string(self, *strings):
        _list = []
        for _string in strings:
            __string_value = _string.lower().strip().replace("\'", "").replace("_", " ")
            __string_value = self.__remove_special_amp(__string_value)
            _list.append(__string_value)
        return _list

    def __remove_special_amp(self, value):
        __string_value = value
        for i in range(10):
            number1 = value.find("&")
            number2 = value.find(";")
            if number1 > -1 and number2 > -1:
                _temp_string = value[number1:number2 + 1:]
                __string_value = value.replace(_temp_string, "")
                for j in range(10):
                    if __string_value.find("  ") > -1:
                        __string_value = __string_value.replace("  ", " ")
                    else:
                        break
            else:
                break
        return __string_value

    def __correct_url(self, url):
        return url.strip()

    def __correct_title(self, title):
        return self.__remove_special_amp(title.strip().replace("_", " "))

    def __get_all_songs(self):
        cn = [self.db.rock_songs.s__rock_song_id, self.db.rock_songs.s__band_id, self.db.rock_songs.s__name,
              self.db.rock_songs.s__title,
              self.db.rock_songs.s__level_top, self.db.rock_songs.s__level_down, self.db.rock_songs.s__telegram_id,
              self.db.rock_songs.s__source_url, self.db.rock_songs.s__time, self.db.rock_songs.s__last_date]
        return db_sql.select_cn_from_t1(self.db.rock_songs.table_name, cn)

    def __update_all_songs(self):
        self.__songs = self.__get_all_songs()

    def __find_all_songs(self, song_name):
        for _song in self.__songs:
            if _song[2] == song_name:
                return _song
        return False

    def __get_band_from_song(self, song):
        band_id = song[1]
        for band in self.__bands:
            if band[0] == band_id:
                return band
        return False

    def __get_all_users(self):
        cn = [self.db.users.s__users_id, self.db.users.s__login, self.db.users.s__telegram_id,
              self.db.users.s__level_top,
              self.db.users.s__level_down, self.db.users.s__date_of_last_activity]
        return db_sql.select_cn_from_t1(self.db.users.table_name, cn)

    def __update_all_users(self):
        self.__users = self.__get_all_users()

    def add_sound(self, name, band, url, time=False):
        title_song = self.__correct_title(name)
        title_band = self.__correct_title(band)
        (name, band) = self.__correct_string(name, band)
        url = self.__correct_url(url)
        if time:
            (time,) = self.__correct_string(time)
        _result = self.__find_all_bands(band)
        if _result:
            self.__add_rock_song(_result[0], name, title_song, url, time)
            return True

        # add band if not find
        self.__add_rock_band(band, title_band)
        self.__update_all_bands()
        # again
        _result = self.__find_all_bands(band)
        if _result:
            self.__add_rock_song(_result[0], name, title_song, url, time)
            return True

        return False

    def find_song(self, name, band):
        (name, band) = self.__correct_string(name, band)
        song = self.__find_all_songs(name)
        if song:
            _band = self.__get_band_from_song(song)
            if _band:
                if band == _band[1]:
                    return True
            # again
            self.__update_all_bands()
            _band = self.__get_band_from_song(song)
            if _band:
                if band == _band[1]:
                    return True
            return False
        # again
        self.__update_all_songs()
        song = self.__find_all_songs(name)
        if song:
            _band = self.__get_band_from_song(song)
            if _band:
                if band == _band[1]:
                    return True
            # again
            self.__update_all_bands()
            _band = self.__get_band_from_song(song)
            if _band:
                if band == _band[1]:
                    return True
            return False
        return False

    def get_song(self, name, band):
        (name, band) = self.__correct_string(name, band)
        band_id = \
            db_sql.select_c1_from_t1_where_c2_eq_v2(self.db.rock_bands.s__rock_band_id, self.db.rock_bands.table_name,
                                                    self.db.rock_bands.s__group_name, band)[0][0]
        cn = [self.db.rock_songs.s__rock_song_id, self.db.rock_songs.s__band_id, self.db.rock_songs.s__name,
              self.db.rock_songs.s__title,
              self.db.rock_songs.s__level_top, self.db.rock_songs.s__level_down, self.db.rock_songs.s__telegram_id,
              self.db.rock_songs.s__source_url, self.db.rock_songs.s__time, self.db.rock_songs.s__last_date]
        tn = [self.db.rock_songs.table_name]
        cc = "{0} = {1} AND {2} = \"{3}\"".format(self.db.rock_songs.s__band_id, band_id, self.db.rock_songs.s__name,
                                                  name)
        return db_sql.select_cn_from_tn_where_complex_condition(cn, tn, cc)

    def get_top_songs(self, last_date, count=50, min_top_value=-1, max_down_value=-1):
        cn = [self.db.rock_songs.s__rock_song_id, self.db.rock_songs.s__band_id, self.db.rock_songs.s__name,
              self.db.rock_songs.s__title,
              self.db.rock_songs.s__level_top, self.db.rock_songs.s__level_down, self.db.rock_songs.s__telegram_id,
              self.db.rock_songs.s__source_url, self.db.rock_songs.s__time, self.db.rock_songs.s__last_date]
        tn = [self.db.rock_songs.table_name]

        cc = "ORDER BY {0} DESC LIMIT {1}".format(self.db.rock_songs.s__level_top, count)
        flag1 = min_top_value > -1
        flag2 = max_down_value > -1
        if flag1:
            cc = "{0} > {1} {2}".format(self.db.rock_songs.s__level_top, min_top_value, cc)
        if flag2:
            if flag1:
                cc = "{0} < {1} AND {2}".format(self.db.rock_songs.s__level_down, max_down_value)
            else:
                cc = "{0} < {1} {2}".format(self.db.rock_songs.s__level_down, max_down_value)

        if flag1 or flag2:
            cc = "{0} < {1} AND {2}".format(self.db.rock_songs.s__last_date, last_date, cc)
        else:
            cc = "{0} < {1} {2}".format(self.db.rock_songs.s__last_date, last_date, cc)
        cc = "{0} != 'telegram_id' AND {1}".format(self.db.rock_songs.s__telegram_id, cc)
        return db_sql.select_cn_from_tn_where_complex_condition(cn, tn, cc)

        # def get_users_activity(self, days=30):
        # Нужно запилить отсев неактивных
        # return self.__users

    def update_song_telegram_id(self, song_id, telegram_id):
        db_sql.update_t1_set_c1_eq_v1_where_c2_eq_v2(self.db.rock_songs.table_name, self.db.rock_songs.s__telegram_id,
                                                     telegram_id, self.db.rock_songs.s__rock_song_id, song_id)

    def update_song_last_date(self, song_id, last_date):
        db_sql.update_t1_set_c1_eq_v1_where_c2_eq_v2(self.db.rock_songs.table_name, self.db.rock_songs.s__last_date,
                                                     last_date, self.db.rock_songs.s__rock_song_id, song_id)

    def update_song_level_down(self, song_id, level_down):
        db_sql.update_t1_set_c1_eq_v1_where_c2_eq_v2(self.db.rock_songs.table_name, self.db.rock_songs.s__level_down,
                                                     level_down, self.db.rock_songs.s__rock_song_id, song_id)

    def update_song_level_top(self, song_id, level_top):
        db_sql.update_t1_set_c1_eq_v1_where_c2_eq_v2(self.db.rock_songs.table_name, self.db.rock_songs.s__level_top,
                                                     level_top, self.db.rock_songs.s__rock_song_id, song_id)

    def update_song_levels(self, song_id, level_top, level_down):
        cvn = "{0} = {1}, {2} = {3}".format(db.rock_songs.s__level_top, level_top,
                                            db.rock_songs.s__level_down, level_down)
        db_sql.update_t1_set_cvn_where_c2_eq_v2(self.db.rock_songs.table_name, cvn,
                                                self.db.rock_songs.s__rock_song_id, song_id)

    def get_all_songs(self):
        return self.__songs

    def get_all_bands(self):
        return self.__bands

    def get_all_users(self):
        return self.__users

    def test(self):
        _string = "adgfads1&amp;134dfgkj"
        print(self.__correct_string(_string))
