from utils.exts import db
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DeviceModel(db.Model):
    """
    设备型号表
    """
    __tablename__ = 'device_model'

    id: int = db.Column(db.Integer, primary_key=True)
    brand: str = db.Column(db.String(64), doc='设备品牌')
    model_name: str = db.Column(db.String(64), doc='型号名称')
    introduce: str = db.Column(db.String(256), doc='型号介绍')
    device_type: str = db.Column(db.String(64), doc='设备类型')
    transport_type: str = db.Column(db.String(64), doc='协议类型')
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


@dataclass
class DeviceSwitch(db.Model):
    """
    智能开关表
    """
    __tablename__ = 'device_switch'

    id: int = db.Column(db.Integer, primary_key=True)
    model_id: int = db.Column(db.Integer, doc='设备型号id')
    device_name: str = db.Column(db.String(64), doc='设备名称')
    device_sn: str = db.Column(db.String(64), doc='设备序列号')
    transport_type: str = db.Column(db.String(64), doc='协议类型')
    ip: str = db.Column(db.String(32), doc='设备IP')
    is_online: int = db.Column(db.Integer, default=0, doc='是否在线')
    way_count: int = db.Column(db.Integer, default=1, doc='几开')
    way1: int = db.Column(db.Integer, default=0, doc='way1状态')
    way2: int = db.Column(db.Integer, default=0, doc='way2状态')
    way3: int = db.Column(db.Integer, default=0, doc='way3状态')
    way4: int = db.Column(db.Integer, default=0, doc='way4状态')
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
