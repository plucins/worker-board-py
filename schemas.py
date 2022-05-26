import enum as _enum
import datetime as _dt
from pydantic.schema import Optional

import pydantic as _pydantic


class _CaseStatus(str, _enum.Enum):
    new = 'new'
    in_progress = 'in_progress'
    close = 'close'


class _EquipmentType(str, _enum.Enum):
    pc = 'pc'
    laptop = 'laptop'
    phone = 'phone'
    other = 'other'


class _UserRole(str, _enum.Enum):
    serviceman = 'serviceman'
    manager = 'manager'
    admin = 'admin'
    customer = 'customer'


class _Owner(_pydantic.BaseModel):
    firstName: str
    lastName: str
    phoneNumber: str


class _Worker(_pydantic.BaseModel):
    firstName: str
    lastName: str


class _Equipment(_pydantic.BaseModel):
    type: _EquipmentType
    mark: str
    model: str
    owner: _Owner

    class Config:
        use_enum_values = True


class _BaseRepairCase(_pydantic.BaseModel):
    title: str
    description: str


class _RepairCase(_BaseRepairCase):
    id: int
    caseStatus: str
    worker: Optional[_Worker]
    registrationTime: _dt.datetime
    lastUpdate: _dt.datetime
    equipment: Optional[_Equipment]

    class Config:
        orm_mode = True


class _CreateRepairCase(_BaseRepairCase):
    pass
