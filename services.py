from typing import TYPE_CHECKING, List
import database as _database
import models as _models
import schemas as _schemas
import fastapi as _fastapi
import datetime as _dt

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


async def create_repair_case(repaircase: _schemas._RepairCase, db: "Session") -> _schemas._RepairCase:
    eqipment_owner = _models.Owner(**repaircase.equipment.owner.dict())
    equipment = _models.Equipment(owner=eqipment_owner, type=repaircase.equipment.type, mark=repaircase.equipment.mark,
                                  model=repaircase.equipment.model)

    repaircase = _models.RepairCase(title=repaircase.title, description=repaircase.description,
                                    equipment=equipment)
    repaircase.caseStatus = _models.CaseStatus.new.value
    db.add(repaircase)
    db.commit()
    db.refresh(repaircase)
    return _schemas._RepairCase.from_orm(repaircase)


async def get_repair_cases(db: "Session") -> List[_schemas._RepairCase]:
    repaircases = db.query(_models.RepairCase).all()
    return list(map(_schemas._RepairCase.from_orm, repaircases))


async def get_repair_cases_by_id(id: int, db: "Session") -> _schemas._RepairCase:
    repaircase = db.query(_models.RepairCase).filter(_models.RepairCase.id == id).first()
    if repaircase is None:
        raise _fastapi.HTTPException(status_code=404, detail="Repair case does not exist")

    return repaircase


async def delete_repair_cases_by_id(id: int, db: "Session"):
    repaircase = await get_repair_cases_by_id(id=id, db=db)
    if repaircase is None:
        raise _fastapi.HTTPException(status_code=404, detail="Repair case does not exist")

    db.delete(repaircase)
    db.commit()


async def create_worker(worker: _schemas._Worker, db: "Session") -> _schemas._Worker:
    worker = _models.Worker(**worker.dict())
    db.add(worker)
    db.commit()
    db.flush()
    db.refresh(worker)
    return _schemas._Worker.from_orm(worker)


async def update_repair_case(id: int, db: "Session", repaircase: _schemas._RepairCase):
    repair_case_to_update = await get_repair_cases_by_id(id=id, db=db)
    if repair_case_to_update is None:
        raise _fastapi.HTTPException(status_code=404, detail="Repair case does not exist")

    repair_case_to_update.lastUpdate = _dt.datetime.now()
    repair_case_to_update.title = repaircase.title
    repair_case_to_update.description = repaircase.description
    repair_case_to_update.caseStatus = repaircase.caseStatus

    if repaircase.worker.id is not None:
        await get_worker_by_id(id=repaircase.worker.id, db=db)
        repair_case_to_update.worker_id = repaircase.worker.id

    db.commit()
    db.refresh(repair_case_to_update)

    return _schemas._RepairCase.from_orm(repair_case_to_update)


async def get_worker_by_id(id: int, db: "Session") -> _schemas._Worker:
    worker = db.query(_models.Worker).filter(_models.Worker.id == id).first()
    if worker is None:
        raise _fastapi.HTTPException(status_code=404, detail="Worker does not exist")

    return worker


async def update_worker(worker: _schemas._Worker, db: "Session") -> _schemas._Worker:
    worker_to_update = await get_worker_by_id(id=worker.id, db=db)
    if worker_to_update is None:
        raise _fastapi.HTTPException(status_code=404, detail="Repair case does not exist")

    worker_to_update.firstName = worker.firstName
    worker_to_update.lastName = worker.lastName

    db.commit()
    db.refresh(worker_to_update)

    return _schemas._Worker.from_orm(worker_to_update)
