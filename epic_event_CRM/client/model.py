import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Client:
    full_name: str
    company_name: str
    email: str
    phone: str
    creation_date: str = datetime.now().strftime("%Y-%m-%d")
    last_update: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_id: int = -1
    collaborator_id: int = -1

    def set_id(self, id):
        self.client_id = id

    @property
    def id(self):
        return self.client_id

    @property
    def id_name(self):
        return "client_id"

    @property
    def name_display(self):
        return self.__repr__()
