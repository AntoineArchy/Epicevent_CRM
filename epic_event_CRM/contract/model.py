import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Contract:
    cost: float
    balance: float
    statut: int = 1
    creation_date: str = datetime.now().strftime("%Y-%m-%d")
    last_update: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contract_id: int = -1
    client_id: int = -1

    def set_id(self, id):
        self.contract_id = id

    @property
    def id(self):
        return self.contract_id

    @property
    def id_name(self):
        return "contract_id"
