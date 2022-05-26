import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from sqlalchemy import MetaData

DATABASE_URL = "postgresql://postgres:root@localhost/postgres"

dbschema = 'workerboard-py'
engine = _sql.create_engine(DATABASE_URL, connect_args={'options': '-csearch_path={}'.format(dbschema)})

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
