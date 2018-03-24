class songs:
    def __init__(self):
        self.__songs = []

    def get_song_by_telegram_id(self, telegram_id):
        for _song in self.__songs:
            if _song.get_telegram_id() == telegram_id:
                return _song
        return False

    def get_song_by_number(self, number):
        return self.__songs[number]

    def append_song(self, song):
        self.__songs.append(song)

    def update_song(self, song):
        _id = song.get_telegram_id()
        counter = 0
        for _song in self.__songs:
            if _song.get_telegram_id() == _id:
                self.__songs[counter] = song
            counter += 1

    def get_length(self):
        return len(self.__songs)

    def remove_song(self, song):
        self.__songs.remove(song)
