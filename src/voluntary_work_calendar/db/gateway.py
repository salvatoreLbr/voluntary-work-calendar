from abc import ABC, abstractmethod
from datetime import date
import pandas as pd
from pathlib import Path
import streamlit as st
from typing import List, Optional, Tuple

from voluntary_work_calendar.auth.password import get_hash, check_rules_password
from voluntary_work_calendar.config import Config
from voluntary_work_calendar.db.crud import get_table, delete_record, create_table
from voluntary_work_calendar.db.local import create_input_path, exist_file
from voluntary_work_calendar.db.main import get_db
from voluntary_work_calendar.db.models import *



class Gateway(ABC):
    @abstractmethod
    def delete_presence(data: date, name: str) -> bool:
        ...
    
    @abstractmethod
    def delete_volunteer(name: str) -> bool:
        ...

    @abstractmethod
    def get_calendar() -> pd.DataFrame:
        ...
    
    @abstractmethod
    def get_user() -> pd.DataFrame:
        ...
    
    @abstractmethod
    def get_volunteers_name() -> List[str]:
        ...

    @abstractmethod
    def insert_new_volunteer(name: str) -> bool:
        ...
    
    @abstractmethod
    def insert_presence(data: date, orario_from: str, orario_to: str, name: str) -> bool:
        ...

    @abstractmethod
    def insert_user(username: str, role: str, clean_password: str) -> bool:
        ...


class DBGateway(Gateway):
    def __init__(self) -> None:
        super().__init__()

    def delete_presence(self, data: date, name: str) -> bool:
        calendar_df = get_table(
            db_session=get_db(),
            model=Calendar,
            filter={
                "data": "=='{}'".format(data),
                "name": "=='{}'".format(name),
            }
        )
        if calendar_df.shape[0] > 0:
            delete_record(
                db_session=get_db(),
                model=Calendar,
                filter={
                    "data": "=='{}'".format(data),
                    "name": "=='{}'".format(name),
                }
            )
            return True
        else:
            st.warning("Il volontario {} non ha inserito la presenza per il {}".format(name, data))
            return False


    def delete_volunteer(self, name: str) -> bool:
        delete_record(
            db_session=get_db(),
            model=Volunteers,
            filter={
                "name": "=='{}'".format(name)
            }
        )
        df = get_table(
            db_session=get_db(),
            model=Volunteers,
            filter={
                "name": "=='{}'".format(name)
            }
        )
        if df.shape[0]==0:
            st.success("Volontario rimosso con successo")
            return True
        else:
            st.warning("!!! Errore !!! Volontario non rimosso dalla lista")
            return False


    def get_calendar(self) -> pd.DataFrame:
        calendar_df = get_table(
            db_session=get_db(),
            model=Calendar
        )
        return calendar_df

    
    def get_user(self) -> pd.DataFrame:
        return get_table(db_session=get_db(), model=Users)
    

    def get_volunteers_name(self) -> List[str]:
        volunteers_df = get_table(
            db_session=get_db(),
            model=Volunteers
        )
        if volunteers_df.shape[0] > 0:
            volunteers_name_list = list(volunteers_df.name)
        else:
            volunteers_name_list = []
        return volunteers_name_list
    

    def insert_new_volunteer(self, name: str) -> bool:
        create_table(
            db_session=get_db(),
            model=Volunteers,
            info=[
                {
                    "name": name,
                }
            ]
        )
        df = get_table(
            db_session=get_db(),
            model=Volunteers,
            filter={
                "name": "=='{}'".format(name)
            }
        )
        if df.shape[0]>0:
            st.success("Volontario aggiunto alla lista")
            return True
        else:
            st.warning("!!! Errore !!! Volontario non aggiunto alla lista")
            return False

    
    def insert_presence(self, data: date, orario_from: str, orario_to: str, name: str) -> bool:
        create_table(
            db_session=get_db(),
            model=Calendar,
            info=[
                {
                    "data": data,
                    "orario_da": orario_from,
                    "orario_a": orario_to,
                    "name": name
                }
            ]
        )
        df = get_table(
            db_session=get_db(),
            model=Calendar,
            filter={
                "data": "=='{}'".format(data),
                "orario_da": "=='{}'".format(orario_from),
                "orario_a": "=='{}'".format(orario_to),
                "name": "=='{}'".format(name)
            }
        )
        if df.shape[0]>0:
            st.success("Presenza inserita")
            return True
        else:
            st.warning("!!! Errore !!! Presenza non inserita")
            return False
    

    def insert_user(self, username: str, role: str, clean_password: str) -> bool:
        error_in_psw, type_response = check_rules_password(clean_password)
        if not error_in_psw:
            create_table(
                db_session=get_db(),
                model=Users,
                info=[
                    {
                        "username": username,
                        "role": role,
                        "hashed_password": get_hash(clean_password),
                    }
                ]
            )
            return True
        else:
            raise Exception(type_response)


class CSVGateway(Gateway):
    def __init__(self, test: Optional[bool]=False) -> None:
        super().__init__()
        self.input_path = create_input_path(test)


    def delete_presence(self, data: date, name: str) -> bool:
        filename, file_path, _, df, _ = self.get_file(table=Calendar)
        idx_to_delete = (df.data == data.strftime("%Y-%m-%d")) & (df.name == name)
        if idx_to_delete.sum() == 0:
            st.warning("Il volontario {} non ha inserito la presenza per il {}".format(name, data))
            return False
        else:
            df = df.drop(idx_to_delete.index[idx_to_delete==True], axis=0).reset_index(drop=True)
            df.to_csv(file_path, index=False)
            text = "Save {} in following path {}".format(filename, file_path)
            print(text)
            return True


    def delete_volunteer(self, name: str) -> bool:
        filename, file_path, _, df, _ = self.get_file(table=Volunteers)
        idx_to_delete = (df.name == name)
        if idx_to_delete.sum() == 0:
            st.warning("!!! Errore !!! Volontario non rimosso dalla lista perchè non presente")
            return False
        else:
            df = df.drop(idx_to_delete.index[idx_to_delete==True], axis=0).reset_index(drop=True)
            st.success("Volontario rimosso con successo")
            df.to_csv(file_path, index=False)
            text = "Save {} in following path {}".format(filename, file_path)
            print(text)
            return True


    def get_calendar(self) -> pd.DataFrame:
        _, _, _, df, _ = self.get_file(table=Calendar)
        return df


    def get_file(self, table: Base) -> Tuple[str, Path, List[str], pd.DataFrame, int]: # type: ignore
        filename = table.__dict__["__tablename__"]+".csv"
        fields = [x for x in list(table.__dict__.keys()) if x[0]!="_"]
        file_path = self.input_path.joinpath(filename)
        if exist_file(file_path):
            df = pd.read_csv(file_path)
            if df.shape[0] > 0:
                starting_id = max(df.id) + 1
            else:
                starting_id = 0
        else:
            text = "Filename {} not exist, will create it".format(filename)
            print(text)
            df = pd.DataFrame([], columns=fields)
            starting_id = 0
        return filename, file_path, fields, df, starting_id


    def get_user(self) -> pd.DataFrame:
        _, _, _, df, _ = self.get_file(table=Users)
        return df


    def get_volunteers_name(self) -> List[str]:
        _, _, _, df, _ = self.get_file(table=Volunteers)
        if df.shape[0] > 0:
            volunteers_name_list = list(df.name)
        else:
            volunteers_name_list = []
        return volunteers_name_list

    def init_csv_gateway(self):
        users_df = self.get_user()
        idx_user = users_df.username == "volontario"
        if idx_user.sum() == 0:
            self.insert_user(
                username=Config.USERNAME_USER,
                role="user",
                clean_password=Config.PSW_USER
            )
            self.insert_user(
                username=Config.USERNAME_ADMIN,
                role="admin",
                clean_password=Config.PSW_ADMIN
            )

    def insert_new_volunteer(self, name: str) -> bool:
        filename, file_path, fields, df, starting_id = self.get_file(table=Volunteers)
        row = pd.DataFrame([[starting_id, name]], columns=fields)
        df = pd.concat([df, row], axis=0)
        df.to_csv(file_path, index=False)
        text = "Save {} in following path {}".format(filename, file_path)
        print(text)
        return True


    def insert_presence(self, data: date, orario_from: str, orario_to: str, name: str) -> bool:
        filename, file_path, fields, df, starting_id = self.get_file(table=Calendar)
        row = pd.DataFrame([[starting_id, data, orario_from, orario_to, name]], columns=fields)
        df = pd.concat([df, row], axis=0)
        df.to_csv(file_path, index=False)
        text = "Save {} in following path {}".format(filename, file_path)
        print(text)
        return True


    def insert_user(self, username: str, role: str, clean_password: str) -> bool:
        filename, file_path, fields, df, starting_id = self.get_file(table=Users)
        error_in_psw, type_response = check_rules_password(clean_password)
        if not error_in_psw:
            row = pd.DataFrame([[starting_id, username, role, get_hash(clean_password)]], columns=fields)
            df = pd.concat([df, row], axis=0)
            df.to_csv(file_path, index=False)
            text = "Save {} in following path {}".format(filename, file_path)
            print(text)
            return True
        else:
            raise Exception(type_response)
