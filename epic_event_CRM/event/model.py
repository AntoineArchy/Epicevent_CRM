import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Event:
    name: str
    event_start: str
    event_end: str
    location: str
    attendees: int
    notes: str
    creation_date: str = datetime.now().strftime("%Y-%m-%d")
    event_id: int = -1
    contract_id: int = -1

    @property
    def id(self):
        return self.event_id

    @property
    def id_name(self):
        return "event_id"
