import pandas as pd
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Union

from voluntary_work_calendar.db import schemas
from voluntary_work_calendar.db.main import Base


######################
#### create funcs ####
######################
def create_table(
    db_session: Session,
    model: Base,  # type: ignore
    info: List[
        Union[schemas.CalendarCreate, schemas.UserInDBCreate, schemas.VolunteersCreate]
    ],
):
    instances = tuple([model(**row) for row in info])

    try:
        db_session.add_all(instances)
        db_session.commit()
        db_session.flush(model)
        # Close session
        db_session.expire_all()
        # Close session
        db_session.close_all()
        print("Table updated!")
        return True, "ok"
    except Exception as e:
        print(f"Eccezione: {e}")
        db_session.rollback()
        db_session.expire_all()
        db_session.close_all()
        print("Table NOT updated!")
        return False, e.__class__.__name__


######################
#### select funcs ####
######################
def get_table(db_session: Session, model: Base, filter: Optional[Dict[str, str]] = None):  # type: ignore
    #: Get table from db
    db_obj = db_session.query(model).all()
    #: Transform obj db in pd.DataFrame
    fields = [x for x in model.__dict__.keys() if x[0]!="_"]
    df = pd.DataFrame([db_row.__dict__ for db_row in db_obj], columns=fields)
    # Close session
    db_session.expire_all()
    db_session.close_all()
    #: Drop _sa_instance_state field if exists
    if "_sa_instance_state" in df.columns:
        df = df.drop(["_sa_instance_state"], axis=1)
    #: Filter if any
    if (filter is not None) & (not df.empty):
        idx_filter = []
        for key, value in filter.items():
            idx_filter.append("(df.{}{}) &".format(key, value))
        idx_filter = "".join(idx_filter)
        idx_filter = idx_filter[:-2]
        df = df.loc[eval(idx_filter)].reset_index(drop=True)
    return df


######################
#### update funcs ####
######################


######################
#### delete funcs ####
######################
def delete_record(db_session: Session, model: Base, filter: Optional[Dict[str, str]] = None):  # type: ignore
    #: Remove records from table's DB
    if filter is not None:
        idx_filter = []
        for key, value in filter.items():
            idx_filter.append("(model.{}{}) &".format(key, value))
        idx_filter = "".join(idx_filter)
        idx_filter = idx_filter[:-2]
        db_session.query(model).filter(eval(idx_filter)).delete(
            synchronize_session="evaluate"
        )
    else:
        db_session.query(model).delete(synchronize_session="evaluate")
    db_session.commit()
    db_session.expire_all()
