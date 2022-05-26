from typing import TYPE_CHECKING, List
import fastapi as _fastapi
from fastapi import FastAPI

import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
async def root():
    _services._create_database()
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/api/repair-case", response_model=_schemas._RepairCase)
async def create_repair_case(repaircase: _schemas._CreateRepairCase,
                             db: _orm.Session = _fastapi.Depends(_services.get_db), ):
    return await _services.create_repair_case(repaircase=repaircase, db=db)


@app.get("/api/repair-case", response_model=List[_schemas._RepairCase])
async def get_repaircases(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_repaircases(db=db)
