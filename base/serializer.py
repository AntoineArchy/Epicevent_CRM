from typing import Dict, Tuple, Callable

from base.model import BaseModel
from epic_event_CRM.collaborator.model import Collaborator


def construct_col_name_for_query(obj_data: Dict) -> str:
    return f"{tuple([*obj_data.keys()])}".replace("'", "")


def construct_val_name_for_query(obj_data: Dict) -> Tuple:
    return tuple([*obj_data.values()])


class BaseSerializer:
    """
    Classe de base pour les sérialiseurs.

    Attributes:
        model (Callable): Modèle utilisé pour la sérialisation.
    """

    model = BaseModel

    @classmethod
    def get_blank_form(cls) -> Dict:
        """
        Retourne un formulaire vide sous forme de dictionnaire.

        Returns:
            Dict: Formulaire vide.
        """
        return vars(cls.model())

    @classmethod
    def get_obj_dict(cls, obj: Callable) -> Dict:
        """
        Retourne le dictionnaire représentant les attributs de l'objet.

        Args:
            obj (Callable): Objet à sérialiser.

        Returns:
            Dict: Dictionnaire représentant les attributs de l'objet.
        """
        return obj.__dict__

    @classmethod
    def from_view_data_to_obj_dict(cls, view_data: Dict) -> Dict:
        """
        Convertit les données de la vue en dictionnaire d'objet.

        Args:
            view_data (Dict): Données de la vue.

        Returns:
            Dict: Dictionnaire d'objet.
        """
        return view_data

    @classmethod
    def from_obj_to_view_data(cls, obj: Callable) -> Dict:
        obj_dict = cls.get_obj_dict(obj)
        return cls.from_obj_dict_to_view_data(obj_dict)

    @classmethod
    def from_obj_dict_to_view_data(cls, obj_dict: Dict) -> Dict:
        return obj_dict
