from typing import TYPE_CHECKING, List
import database as _database
import models as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_repair_case(repaircase: _schemas._CreateRepairCase, db: "Session") -> _schemas._RepairCase:
    repaircase = _models.RepairCase(**repaircase.dict())
    repaircase.caseStatus = _schemas._CaseStatus.new.value
    db.add(repaircase)
    db.commit()
    db.refresh(repaircase)
    return _schemas._RepairCase.from_orm(repaircase)


async def get_repaircases(db: "Session") -> List[_schemas._RepairCase]:
    repaircases = db.query(_models.RepairCase).all()
    return list(map(_schemas._RepairCase.from_orm, repaircases))
