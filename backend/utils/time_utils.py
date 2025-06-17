import datetime
import pytz

FIRST_DAY_OF_WEEK = 0

class TimeUtils:
    @classmethod
    def get_current_vn_time(cls):
        utcnow = datetime.datetime.utcnow()
        return pytz.timezone('Asia/Ho_Chi_Minh').utcoffset(utcnow) + utcnow

    @classmethod
    def get_second_wait(cls):
        # second_point = 5
        current_date = TimeUtils.get_current_vn_time()
        current_second = current_date.second % 10  # Tìm phần dư khi chia cho 10
        if current_second in [4,5,6,7,8,9]:
            time_sleep_remain = 0
        else: # current_second in [0,1,2,3,4,5,6]:
            time_sleep_remain = 4 - current_second

        return time_sleep_remain

    @classmethod
    def get_latest_bctc_period(cls):
        now = datetime.datetime.now()
        quarter = (now.month - 1) // 3 + 1

        if quarter == 1:
            return now.year - 1, 4
        return now.year, quarter - 1