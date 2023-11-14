from dataclasses import dataclass
from typing import List, Any, Dict


@dataclass
class BaseModel:
    Field1: Any = "No data"
    Field2: Any = "No data"
    args: List = None
    kwargs: Dict = None
    obj_id: int = -1

    @property
    def id(self):
        return self.obj_id

    @property
    def id_name(self):
        return "obj_id"

    @property
    def name_display(self):
        return self.__repr__()
