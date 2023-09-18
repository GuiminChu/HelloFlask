from flask_sqlalchemy import SQLAlchemy
from flask.json.provider import DefaultJSONProvider
from flask_jwt_extended import JWTManager
from datetime import datetime
from utils.func import Func

db = SQLAlchemy()

jwt = JWTManager()


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        print(f'CustomJSONProvider ----------------- {type(obj)}')

        if hasattr(obj, '__table__'):
            camel_case_dict = {}
            for column in obj.__table__.columns:
                camel_case_key = Func.snake_to_camel(column.name)
                camel_case_dict[camel_case_key] = getattr(obj, column.name)
            return camel_case_dict

        if isinstance(obj, dict):
            camel_case_dict = {}
            for key, value in obj.items():
                camel_case_key = Func.snake_to_camel(key)
                camel_case_dict[camel_case_key] = value
            return camel_case_dict

        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        return super().default(obj)
