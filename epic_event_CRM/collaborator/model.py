import dataclasses
from datetime import datetime

import bcrypt

from base import roles
from utils import hash_password


@dataclasses.dataclass
class Collaborator:
    department: str = "collaborator"
    first_name: str = "John"
    last_name: str = "Doe"
    username: str = "JDoe"
    password: str = "secret"
    creation_date: str = datetime.now().strftime("%Y-%m-%d")
    last_update: str = datetime.now().strftime("%Y-%m-%d")
    collaborator_id: int = -1
    is_active: bool = True

    def set_id(self, id):
        self.collaborator_id = id

    @property
    def id(self):
        return self.collaborator_id

    @property
    def id_name(self):
        return "collaborator_id"

    def has_role(self, role):
        return (
            role == roles.EpicEventRole[self.department.lower()]
            or role == roles.EpicEventRole.collaborator
        )

    def set_password(self):
        hashed_password_str = hash_password(self.password)
        self.password = hashed_password_str

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)
