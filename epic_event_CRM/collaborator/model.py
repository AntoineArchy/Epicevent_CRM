import dataclasses
from datetime import datetime

from epic_event_CRM.base.roles import EpicEventRole


@dataclasses.dataclass
class Collaborator:
    department: str = "collaborator"
    first_name: str = "John"
    last_name: str = "Doe"
    username: str = "JDoe"
    password: str = "secret"
    creation_date: str = datetime.now().strftime("%Y-%m-%d")
    collaborator_id: int = -1

    @property
    def id(self):
        return self.collaborator_id

    @property
    def id_name(self):
        return "collaborator_id"

    def has_role(self, role):
        return (
            role == EpicEventRole[self.department.lower()]
            or role == EpicEventRole.collaborator
        )
