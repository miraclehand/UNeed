import sys
sys.path.append('../../commons/utils')

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from singleton import SingletonInstance

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

shed = Scheduler.instance()

