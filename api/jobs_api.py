from flask import Blueprint, request
from flask_apscheduler import APScheduler


def init():
    global scheduler
    scheduler = APScheduler()
    return scheduler

def add_job():
    scheduler.add_job()
    pass