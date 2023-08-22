# https://viniciuschiele.github.io/flask-apscheduler/index.html
from flask_apscheduler import APScheduler
from concurrent.futures import ThreadPoolExecutor
from utils.logger import logger
from utils.exts import db
from model.entity.smart_task_model import SmartTaskModel

scheduler = APScheduler()

# 创建线程池执行器
executor = ThreadPoolExecutor(2)


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

    JOBS = [
        {
            'id': 'do_job_2',
            'func': 'utils.jobs:test_job_2',
            'args': (2,),
            'trigger': 'interval',  # date interval cron
            'seconds': 3,
            'start_date': '2023-01-01 12:10:00'
        }
    ]


def read_db_background():
    pass


def read_db():
    select = db.select(SmartTaskModel).where(SmartTaskModel.is_deleted == 0)
    users = db.session.execute(select).all()
    scheduler.add_job()


@scheduler.task('interval', id='do_job_1', seconds=3)
def test_job_1():
    logger.info('定时任务1')


def test_job_2(param):
    logger.info('定时任务' + str(param))


def test_job_3(param):
    logger.info(f'定时任务{param}')


def device_task():
    """
    设备定时任务
    """
    pass


def scene_task():
    """
    场景定时任务
    """
    pass
