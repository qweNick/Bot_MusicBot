import random
import sqlite3
import telebot
from telebot import types
import threading
import time
from system_music.bot import bot_config
from db_sqlite.db_control.db_control_core import db_control_core
from system_music.classes.current_date import current_date
from system_music.classes.songs import songs as class_songs
from system_music.classes.song import song

_chat_id = "456905705"
_channel_id = "456905705"


class core:
    db_cc = db_control_core()
    bot = telebot.TeleBot(bot_config.token)
    c_d = current_date()
    songs = class_songs()
    songs_top = class_songs()

    count_of_songs_per_time = 2
    repeat_songs_through_count_days = 50
    periodicity = 1800

    global_work = True

    def threads_start(self):
        list_methods = [self.thread_time, self.thread_top_songs, self.thread_bot_publish_songs, self.thread_final_song]
        _thread = threading.Thread(target=self.thread_execution_every_hour, args=(list_methods,))
        _thread.start()
        _thread_bot = threading.Thread(target=self.thread_bot_polling)
        _thread_bot.start()

    def thread_bot_polling(self):
        self.bot.polling(none_stop=True, timeout=50)

    def thread_execution_every_hour(self, list_methods):
        while self.global_work:
            for method in list_methods:
                method()
            time.sleep(self.periodicity)

    def thread_time(self):
        self.c_d.update_current_day()
        self.send_log("Current day: {0}".format(self.c_d.get_current_day()))

    def thread_top_songs(self):
        try:
            self.songs_top = class_songs()
            top_date = self.c_d.get_current_day() - self.repeat_songs_through_count_days
            if top_date < 0:
                top_date = 1
            top_songs = self.db_cc.get_top_songs(last_date=top_date, max_down_value=0)
            if len(top_songs) > 0:
                result_message = "Top songs:"
                for _song in top_songs:
                    __song = song(_song)
                    self.songs_top.append_song(__song)
                    result_message = "{0} \n [{1}][{2}][{3}]".format(result_message, __song.get_song_id(),
                                                                     __song.get_title(),
                                                                     __song.get_last_date())
            else:
                result_message = "Top songs is empty"
        except sqlite3.DatabaseError as _error:
            result_message = "----- Error (db_cc.get_top_songs [{0}])".format(_error)
        self.send_log(result_message)

    def thread_bot_publish_songs(self):
        try:
            count_songs = self.songs_top.get_length()
            for i in range(self.count_of_songs_per_time):
                random_number = random.randrange(0, count_songs)
                _song = self.songs_top.get_song_by_number(random_number)

                keyboard = types.InlineKeyboardMarkup()
                callback_button_plus = types.InlineKeyboardButton(text="✌ 0", callback_data="+1")
                callback_button_minus = types.InlineKeyboardButton(text="Drop 0", callback_data="-1")
                keyboard.add(callback_button_plus, callback_button_minus)
                result = self.bot.send_audio(chat_id=_channel_id, audio=_song.get_telegram_id(),
                                             caption=_song.get_title(), reply_markup=keyboard)
                _song.set_message_telegram_id(result.message_id)
                _song.set_last_date(self.c_d.get_current_day())
                self.songs.append_song(_song)
                self.db_cc.update_song_last_date(_song.get_song_id(), self.c_d.get_current_day())
                # self.send_log(result.message_id)
        except:
            self.send_log("----- Error (thread_bot_publish_songs) ")

    def thread_final_song(self):
        _current_date = self.c_d.get_current_day()
        _songs_length = self.songs.get_length()
        for number in range(0, _songs_length):
            _song = self.songs.get_song_by_number(number)
            if _song:
                if _current_date - _song.get_last_date() > 5:
                    _song_level_top = _song.get_level_top_old()
                    if _song_level_top < _song.get_level_top():
                        _song_level_top = _song.get_level_top()
                    _song_level_down = _song.get_level_down_old()
                    if _song_level_down < _song.get_level_down():
                        _song_level_down = _song.get_level_down_old()
                    self.db_cc.update_song_levels(_song.get_song_id(), _song_level_top, _song_level_down)
                    try:
                        self.bot.edit_message_caption(chat_id=_channel_id, message_id=_song.get_message_telegram_id(),
                                                      caption=_song.get_title())
                    except:
                        self.send_log("----- Error (thread_final_song)")

    def send_log(self, text_message):
        try:
            self.bot.send_message(chat_id=_chat_id, text=text_message)
        except:
            print("----- Error (send_log) \n [{0}]".format(text_message))
            # print(text_message)
            # time.sleep(1)


@core.bot.message_handler(content_types=["text"])
def any_commands(message):
    if message.text.find("// global stop") > -1:
        _songs_length = core.songs.get_length()
        for number in range(0, _songs_length):
            _song = core.songs.get_song_by_number(number)
            if _song:
                _song_level_top = _song.get_level_top_old()
                if _song_level_top < _song.get_level_top():
                    _song_level_top = _song.get_level_top()
                _song_level_down = _song.get_level_down_old()
                if _song_level_down < _song.get_level_down():
                    _song_level_down = _song.get_level_down_old()
                core.db_cc.update_song_levels(_song.get_song_id(), _song_level_top, _song_level_down)
                try:
                    core.bot.edit_message_caption(chat_id=_channel_id, message_id=_song.get_message_telegram_id(),
                                                  caption=_song.get_title())
                except:
                    core.send_log(core, "----- Error (any_commands)")
        core.global_work = False
        core.bot.stop_polling()
        core.send_log(core, "Success stop")

    if message.text.find("// count_of_songs_per_time") > -1:
        _value = message.text[26:]
        _value.split()
        try:
            _value = int(_value)
            core.count_of_songs_per_time = _value
            core.send_log(core, "Success change count_of_songs_per_day = {0}".format(_value))
        except:
            core.send_log(core, "----- Error (any_commands [ // count_of_songs_per_time {0} ])".format(_value))

    if message.text.find("// periodicity") > -1:
        _value = message.text[14:]
        _value.split()
        try:
            _value = int(_value)
            core.periodicity = _value
            core.send_log(core, "Success change periodicity = {0}".format(_value))
        except:
            core.send_log(core, "----- Error (any_commands [ // periodicity {0} ])".format(_value))

    if message.text.find("// repeat_songs_through_count_days") > -1:
        _value = message.text[34:]
        _value.split()
        try:
            _value = int(_value)
            core.repeat_songs_through_count_days = _value
            core.send_log(core, "Success change repeat_songs_through_count_days = {0}".format(_value))
        except:
            core.send_log(core, "----- Error (any_commands [ // repeat_songs_through_count_days {0} ])".format(_value))

            # keyboard = types.InlineKeyboardMarkup()
            # callback_button_plus = types.InlineKeyboardButton(text="✌ " + str(counter.counter_top), callback_data="+1")
            # callback_button_minus = types.InlineKeyboardButton(text="Drop " + str(counter.counter_down),
            #                                                    callback_data="-1")
            # keyboard.add(callback_button_plus, callback_button_minus)
            # result = bot.send_message(message.chat.id, "Музыка", reply_markup=keyboard)
            # core.send_log(core, "some text")
            # print(result)


@core.bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "+1":
            _song = core.songs.get_song_by_telegram_id(call.message.audio.file_id)
            if _song:
                if _song.find_by_user_id(call.from_user.id):
                    return
                _song.rise_level_top()
                _song.add_voted_user_id(call.from_user.id)
                core.songs.update_song(_song)

                keyboard = types.InlineKeyboardMarkup()
                callback_button_plus = types.InlineKeyboardButton(text="Rise " + str(_song.get_level_top()),
                                                                  callback_data="+1")
                callback_button_minus = types.InlineKeyboardButton(text="Drop " + str(_song.get_level_down()),
                                                                   callback_data="-1")
                keyboard.add(callback_button_plus, callback_button_minus)
                try:
                    core.bot.edit_message_caption(chat_id=_channel_id, message_id=call.message.message_id,
                                                  reply_markup=keyboard, caption=_song.get_title())
                except:
                    core.send_log(core, "----- Error (callback_inline)")
            else:
                core.send_log(core, "----- Error (callback_inline) [song not find]")
            # print(result)

        if call.data == "-1":
            _song = core.songs.get_song_by_telegram_id(call.message.audio.file_id)
            if _song:
                if _song.find_by_user_id(call.from_user.id):
                    return
                _song.rise_level_down()
                _song.add_voted_user_id(call.from_user.id)
                core.songs.update_song(_song)

                keyboard = types.InlineKeyboardMarkup()
                callback_button_plus = types.InlineKeyboardButton(text="Rise " + str(_song.get_level_top()),
                                                                  callback_data="+1")
                callback_button_minus = types.InlineKeyboardButton(text="Drop " + str(_song.get_level_down()),
                                                                   callback_data="-1")
                keyboard.add(callback_button_plus, callback_button_minus)
                try:
                    core.bot.edit_message_caption(chat_id=_channel_id, message_id=call.message.message_id,
                                                  reply_markup=keyboard, caption=_song.get_title())
                except:
                    core.send_log(core, "----- Error (callback_inline)")
            else:
                core.send_log(core, "----- Error (callback_inline) [song not find]")
            # print(result)




            # if call.data == "-1":
            #     core.counter = counter.counter_down - 1
            # keyboard = types.InlineKeyboardMarkup()
            # callback_button_plus = types.InlineKeyboardButton(text="Rise " + str(counter.counter_top),
            #                                                   callback_data="+1")
            # callback_button_minus = types.InlineKeyboardButton(text="Drop " + str(counter.counter_down),
            #                                                    callback_data="-1")
            # keyboard.add(callback_button_plus, callback_button_minus)
            # result = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                                text="Музыка", reply_markup=keyboard)
            # print(result.date)
