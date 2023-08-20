# https://viniciuschiele.github.io/flask-apscheduler/index.html
from flask_apscheduler import APScheduler
from utils.logger import logger

scheduler = APScheduler()


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

    JOBS = [
        {
            'id': 'do_job_2',
            'func': 'utils.jobs:test_job_2',
            # 'args': (1, 2),
            'trigger': 'interval',  # date interval cron
            'seconds': 3,
            'start_date': '2023-01-01 12:10:00'
        }
    ]


@scheduler.task('interval', id='do_job_1', seconds=3)
def test_job_1():
    logger.info('定时任务1')


def test_job_2():
    logger.info('定时任务2')
