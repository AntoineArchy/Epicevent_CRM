from dataclasses import dataclass
from typing import List, Any, Dict


@dataclass
class BaseModel:
    Field1: Any = "No data"
    Field2: Any = "No data"
    args: List = None
    kwargs: Dict = None
    obj_id: int = -1

    def set_id(self, id):
        """
        Définit l'identifiant unique de l'objet.

        Args:
            id: Identifiant de l'objet.

        Returns:
            None
        """
        self.obj_id = id

    @property
    def id(self):
        """
        Propriété représentant l'identifiant unique de l'objet.

        Returns:
            int: Identifiant de l'objet.
        """
        return self.obj_id

    @property
    def id_name(self):
        """
        Propriété représentant le nom de l'attribut identifiant unique.

        Returns:
            str: Nom de l'attribut identifiant.
        """
        return "obj_id"

    @property
    def name_display(self):
        """
        Propriété représentant l'affichage d'un de l'objet.

        Returns:
            str: Affichage de l'objet.
        """
        return self.__repr__()
