from typing import TYPE_CHECKING, List
import fastapi as _fastapi
from fastapi import FastAPI

import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/api/repair-case", response_model=_schemas._RepairCase)
async def create_repair_case(repaircase: _schemas._RepairCase,
                             db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_repair_case(repaircase=repaircase, db=db)


@app.get("/api/repair-case", response_model=List[_schemas._RepairCase])
async def get_repair_cases(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_repair_cases(db=db)


@app.get("/api/repair-case/{id}", response_model=_schemas._RepairCase)
async def get_repair_cases_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_repair_cases_by_id(id=id, db=db)


@app.delete("/api/repair-case/{id}")
async def delete_repair_cases_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_repair_cases_by_id(id=id, db=db)
    return "ok"


@app.post("/api/worker", response_model=_schemas._Worker)
async def create_worker(worker: _schemas._Worker, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_worker(worker=worker, db=db)


@app.put("/api/repair-case/{id}", response_model=_schemas._RepairCase)
async def update_repair_case(id: int, repaircase: _schemas._RepairCase,
                             db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.update_repair_case(id=id, db=db, repaircase=repaircase)


@app.get("/api/workers", response_model=List[_schemas._Worker])
async def get_workers(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_workers(db=db)


@app.get("/api/worker/{id}", response_model=_schemas._Worker)
async def get_worker_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_worker_by_id(id=id, db=db)


@app.delete("/api/worker/{id}")
async def delete_worker_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_worker_by_id(id=id, db=db)
    return "ok"


@app.put("/api/worker/{id}", response_model=_schemas._Worker)
async def update_worker(id: int, worker: _schemas._Worker,
                        db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.update_worker_self(id=id, db=db, worker=worker)


@app.post("/api/owner", response_model=_schemas._Owner)
async def create_owner(owner: _schemas._Owner, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_owner(owner=owner, db=db)


@app.get("/api/owners", response_model=List[_schemas._Owner])
async def get_owners(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_owners(db=db)


@app.get("/api/owner/{id}", response_model=_schemas._Owner)
async def get_owner_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_owner_by_id(id=id, db=db)


@app.delete("/api/owner/{id}")
async def delete_owner_by_id(id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    await _services.delete_owner_by_id(id=id, db=db)
    return "ok"


@app.put("/api/owner/{id}", response_model=_schemas._Owner)
async def update_owner(id: int, owner: _schemas._Owner,
                        db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.update_owner(id=id, db=db, owner=owner)
