from flask import current_app
import redis


class Redis(object):

    @staticmethod
    def _get_r():
        rf = current_app.config.get('redis')
        host = rf['host']
        port = rf['port']
        db = rf['database']
        pwd = rf['password']
        r = redis.StrictRedis(host, port, db, pwd)
        return r

    @classmethod
    def set(cls, key, value):
        r = cls._get_r()
        r.set(key, value)
