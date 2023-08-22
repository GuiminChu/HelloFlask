from utils.exts import db
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SmartTaskModel(db.Model):
    """
    定时任务表
    """
    __tablename__ = 'smart_task'

    id: int = db.Column(db.Integer, primary_key=True)
    target_id: int = db.Column(db.Integer, doc='目标id')
    type: str = db.Column(db.String(64), doc='设备或场景')
    trigger: str = db.Column(db.String(64))
    create_user: int = db.Column(db.Integer, doc='创建人')
    create_time: str = db.Column(db.DateTime, default=datetime.now, doc='创建时间')
    update_user: int = db.Column(db.Integer, doc='更新人')
    update_time: str = db.Column(db.DateTime, default=datetime.now, doc='更新时间')
    is_deleted: int = db.Column(db.Boolean, default=False, doc='是否删除')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def from_dict(cls, dictionary):
        instance = cls()
        for key, value in dictionary.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
