from utils.exts import db
from datetime import datetime

# https://segmentfault.com/a/1190000042881840
# SQLAlchemy 数据模型序列化（转JSON）
from dataclasses import dataclass


@dataclass
class UserModel(db.Model):
    # 指定模型类对应的数据库表名。如果不指定，则默认为类名的小写形式。
    __tablename__ = 'user'

    id: int = db.Column(db.Integer, primary_key=True)
    account: str = db.Column(db.String(20), unique=True, nullable=False, doc='账号')
    password: str = db.Column(db.String(20), doc='密码')
    name: str = db.Column(db.String(20), doc='昵称')
    avatar: str = db.Column(db.String(200), doc='头像')
    phone: str = db.Column(db.String(20), doc='手机号')
    birthday: str = db.Column(db.DateTime, doc='生日')
    sex: int = db.Column(db.Integer, doc='性别')
    create_time: str = db.Column(db.DateTime, default=datetime.now, doc='创建时间')
    update_time: str = db.Column(db.DateTime, default=datetime.now, doc='更新时间')
    is_deleted: int = db.Column(db.Boolean, default=False, doc='是否删除')

    def save(self):
        db.session.add(self)
        db.session.commit()
