from typing import TYPE_CHECKING, List
import database as _database
import models as _models
import schemas as _schemas
import fastapi as _fastapi

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
    repaircase.caseStatus = _models.CaseStatus.new.value
    db.add(repaircase)
    db.commit()
    db.refresh(repaircase)
    return _schemas._RepairCase.from_orm(repaircase)


async def get_repair_cases(db: "Session") -> List[_schemas._RepairCase]:
    repaircases = db.query(_models.RepairCase).all()
    return list(map(_schemas._RepairCase.from_orm, repaircases))


async def get_repair_cases_by_id(id: int, db: "Session"):
    repaircase = db.query(_models.RepairCase).filter(_models.RepairCase.id == id).first()
    if repaircase is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")

    return repaircase


async def delete_repair_cases_by_id(id: int, db: "Session"):
    repaircase = await get_repair_cases_by_id(id=id, db=db)
    if repaircase is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")

    db.delete(repaircase)
    db.commit()
