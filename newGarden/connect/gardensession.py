from datetime import datetime
from sqlite3 import connect, Error
from typing import Optional

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import Session

from model import Plant, Lifeline, Requirement, PluginCore

_DB_PATH = '/newGarden/garden.db'
_DB_URL_TEMPLATE = "sqlite://{}"


class GardenSession:
    DB_PATH = '/datadb/garden.db'

    def __init__(self, db_path: str = _DB_URL_TEMPLATE.format(DB_PATH)):
        self._engine = create_engine(
            db_path,
            echo=True
        )
        self._exact_session = Session(bind=self._engine)

    def get_all_plant(self):
        return self.exact_session.query(Plant).all()

    def get_plant_by_id(self, plant_id: int):
        return self._get_by_id(Plant, plant_id)

    def get_lifeline_by_id(self, lifeline_id: int):
        return self._get_by_id(Lifeline, lifeline_id)

    def get_requirement_by_id(self, requirement_id: str):
        return self._get_by_id(Requirement, requirement_id)

    def get_plugincore_by_requirement(self, requirement: Requirement):
        return self._search_by(PluginCore, requirement_name=requirement.id)[0]

    def get_plant_lifelines(self, plant_id: int):
        return list(self.exact_session.query(Lifeline).filter(Lifeline.plant_id == plant_id))

    def get_plant_lifeline(self, plant_id: int, lifeline_id: int):
        return (
            self.exact_session
                .query(Lifeline)
                .filter(Lifeline.plant_id == plant_id).filter(Lifeline.id == lifeline_id).one_or_none()
        )

    def is_plant_exists(self, plant_id: int):
        return self._is_exists(Plant, plant_id)

    def init_actual_session(self):
        self._exact_session = Session(bind=self._engine)

    @property
    def exact_session(self):
        return self._exact_session

    def close(self):
        self._exact_session.close()
        self._exact_session = None

    def _get_by_id(self, model_class, instance_id):
        return self.exact_session.query(model_class).get(instance_id)

    def _search_by(self, model_class, **kwargs):
        return self.exact_session.query(model_class).filter_by(**kwargs)

    def _is_exists(self, model_class, instance_id: int):
        return self.exact_session.query(exists().where(model_class.id == instance_id)).scalar()

    def add(self, instance, *, auto_commit: bool = True):
        self.exact_session.add(instance)
        if auto_commit:
            self.exact_session.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exact_session.commit()
        self.close()


class GardenSessionProvider:

    def __init__(self, db_path: str = _DB_PATH):
        self._db_path = db_path

    def provide_session(self) -> GardenSession:
        return GardenSession(_DB_URL_TEMPLATE.format(self._db_path))
