import datetime

X_DAY = 1
X_MONTH = 3
X_YEAR = 2018


class current_date:
    def __init__(self):
        now = datetime.date.today()
        self.__x_day = datetime.date(X_YEAR, X_MONTH, X_DAY)
        self.__current_day = (now - self.__x_day).days

    def get_current_day(self):
        return self.__current_day

    def update_current_day(self):
        self.__current_day = (datetime.date.today() - self.__x_day).days
        # while True:
        #     now = datetime.date.today()
        #     if now > self.__now:
        #         self.__current_day = (now - self.__x_day).days
        #     time.sleep(3600 - datetime.datetime.now().minute * 60 + 1)
