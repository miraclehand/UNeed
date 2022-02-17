from apscheduler.schedulers.background import BackgroundScheduler
from fake_useragent import UserAgent
import atexit

class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class Scheduler(SingletonInstance):
    _sched = BackgroundScheduler({'apscheduler.timezone': 'Asia/Seoul'})
    _sched.start()

    def __init__(self):
        atexit.register(lambda: self._sched.shutdown(wait=False))

    def add_cron_job(self, job, day, hour, minute):
        self._sched.add_job(job,'cron',day_of_week=day,hour=hour,minute=minute)

    def add_interval_job(self, job, seconds, job_name):
        self._sched.add_job(job, 'interval', seconds=seconds, id=job_name)

    def remove_job(self, job_id):
        if self._sched.get_job(job_id):
            self._sched.remove_job(job_id)

    def remove_all(self):
        for job in self._sched.get_jobs():
            self.remove_job(job.id)

class Corps(SingletonInstance):
    _corps = list()

    def clear(self):
        self._corps = list()

    def is_empty(self):
        return not self._corps
        
    def get(self, corp_code):
        for corp in self._corps:
            if corp.findtext('corp_code') == corp_code:
                return corp
        return None

    def set(self, corps):
        self._corps = corps

class FakeUserAgent(SingletonInstance):
    #_ua = UserAgent(use_cache_server=False, verify_ssl=False)
    _ua = UserAgent(verify_ssl=False)
    #_ua = UserAgent()

    def random(self):
        return self._ua.random

class OpenDart(SingletonInstance):
    _count  = 0
    _kospi  = dict()
    _kosdaq = dict()

    def set_total_count(self, count):
        self._count = count

    def set_kospi(self, kospi):
        self._kospi = kospi

    def set_kosdaq(self, kosdaq):
        self._kosdaq = kosdaq

    def get_total_count(self):
        return self._count

    def get_kospi(self):
        return self._kospi

    def get_kosdaq(self):
        return self._kosdaq

    def clear(self):
        self._kospi  = dict()
        self._kosdaq = dict()

class OHLCV(SingletonInstance):
    _ohlcv = dict()

    def clear(self):
        self._ohlcv = dict()

    def get(self, code):
        if code in self._ohlcv:
            return self._ohlcv[code]
        return None

    def set(self, code, df):
        self._ohlcv[code] = df

class Ticks(SingletonInstance):
    _ticks = dict()

    def clear(self):
        self._ticks = dict()

    def get(self, code):
        if code in self._ticks:
            return self._ticks[code]
        return None

    def set(self, code, df):
        self._ticks[code] = df

class StdDisc(SingletonInstance):
    _std_disc = dict()

    def clear(self):
        self._std_disc = dict()

    def count(self):
        return self._std_disc.keys().__len__()

    def get(self, report_nm):
        for key in self._std_disc.keys():
            for keyword in self._std_disc[key].keyword.split('|'):
                if keyword in report_nm:
                    return self._std_disc[key]
        return None

    def set(self, new_std_disc):
        key = new_std_disc._id
        self._std_disc[key] = new_std_disc

od = OpenDart.instance()
ua = FakeUserAgent.instance()
shed = Scheduler.instance()
pool_corps = Corps.instance()
pool_ohlcv = OHLCV.instance()
pool_ticks = Ticks.instance()
pool_std_discs = StdDisc.instance()
