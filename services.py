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
        raise _fastapi.HTTPException(status_code=404, detail="Worker case does not exist")

    worker_to_update.firstName = worker.firstName
    worker_to_update.lastName = worker.lastName

    db.commit()
    db.refresh(worker_to_update)

    return _schemas._Worker.from_orm(worker_to_update)


async def get_workers(db):
    workers = db.query(_models.Worker).all()
    return list(map(_schemas._Worker.from_orm, workers))


async def delete_worker_by_id(id: int, db: "Session"):
    worker = await get_worker_by_id(id=id, db=db)
    if worker is None:
        raise _fastapi.HTTPException(status_code=404, detail="Worker case does not exist")

    db.delete(worker)
    db.commit()


async def update_worker_self(id: int, db: "Session", worker: _schemas._Worker):
    worker_to_update = await get_worker_by_id(id=id, db=db)
    if worker_to_update is not None:
        worker_to_update.firstName = worker.firstName
        worker_to_update.lastName = worker.lastName

        db.commit()
        db.refresh(worker_to_update)

    return _schemas._Worker.from_orm(worker_to_update)


async def create_owner(owner: _schemas._Owner, db: "Session") -> _schemas._Owner:
    owner = _models.Owner(**owner.dict())
    db.add(owner)
    db.commit()
    db.flush()
    db.refresh(owner)
    return _schemas._Owner.from_orm(owner)


async def get_owners(db: "Session"):
    owners = db.query(_models.Owner).all()
    return list(map(_schemas._Owner.from_orm, owners))


async def get_owner_by_id(id: int, db: "Session") -> _schemas._Owner:
    owner = db.query(_models.Owner).filter(_models.Owner.id == id).first()
    if owner is None:
        raise _fastapi.HTTPException(status_code=404, detail="Owner does not exist")

    return owner


async def delete_owner_by_id(id: int, db: "Session"):
    owner = await get_worker_by_id(id=id, db=db)
    if owner is None:
        raise _fastapi.HTTPException(status_code=404, detail="Owner case does not exist")

    db.delete(owner)
    db.commit()


async def update_owner(id: int, db: "Session", owner: _schemas._Owner):
    owner_to_update = await get_owner_by_id(id=id, db=db)
    if owner_to_update is not None:
        owner_to_update.firstName = owner.firstName
        owner_to_update.lastName = owner.lastName
        owner_to_update.phoneNumber = owner.phoneNumber

        db.commit()
        db.refresh(owner_to_update)

    return _schemas._Owner.from_orm(owner_to_update)
