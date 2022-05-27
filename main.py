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
