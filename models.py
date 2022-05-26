import datetime as _dt
import sqlalchemy as _sql
import enum
from sqlalchemy.orm import relationship, backref

import database as _database


class CaseStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    close = "close"


class EquipmentType(enum.Enum):
    pc = "pc"
    laptop = "laptop"
    phone = "phone"
    other = "other"


class UserRole(enum.Enum):
    serviceman = "serviceman"
    manager = "manager"
    admin = "admin"
    customer = "customer"


class Owner(_database.Base):
    __tablename__ = 'owner'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstName = _sql.Column(_sql.String, nullable=False)
    lastName = _sql.Column(_sql.String, nullable=False)
    phoneNumber = _sql.Column(_sql.String, nullable=False)


class Worker(_database.Base):
    __tablename__ = 'worker'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstName = _sql.Column(_sql.String, nullable=False)
    lastName = _sql.Column(_sql.String, nullable=False)


class Equipment(_database.Base):
    __tablename__ = 'equipment'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    type = _sql.Column(_sql.Enum(EquipmentType))
    mark = _sql.Column(_sql.String, nullable=False)
    model = _sql.Column(_sql.String, nullable=False)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('owner.id'), unique=True)
    owner = relationship("Owner", backref=backref("repair-case", uselist=False))


class RepairCase(_database.Base):
    __tablename__ = 'repair-case'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=False)
    caseStatus = _sql.Column('caseStatus', _sql.String)
    worker_id = _sql.Column(_sql.Integer, _sql.ForeignKey('worker.id'), unique=True)
    worker = relationship("Worker", backref=backref("repair-case", uselist=False))
    registrationTime = _sql.Column(_sql.DateTime, default=_dt.datetime.now())
    lastUpdate = _sql.Column(_sql.DateTime, default=_dt.datetime.now())
    equipment_id = _sql.Column(_sql.Integer, _sql.ForeignKey('equipment.id'), unique=True)
    equipment = relationship("Equipment", backref=backref("repair-case", uselist=False))
