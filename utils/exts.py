from flask_sqlalchemy import SQLAlchemy
from flask.json.provider import DefaultJSONProvider
from datetime import datetime

db = SQLAlchemy()


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)
