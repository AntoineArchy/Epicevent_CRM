from __future__ import annotations

from typing import List, Tuple

from base import authorization
from epic_event_CRM.collaborator.model import Collaborator
from base.context import Context


def set_table_allias(fields: List | None, field_display: List | None) -> str:
    """
    Construit la chaîne des alias pour les champs de la table dans la requête SQL.

    Args:
        fields (List | None): Liste des noms de champ.
        field_display (List | None): Liste des noms d'alias pour les champs.

    Returns:
        str: Chaîne des alias pour les champs de la table.
    """
    if fields is None:
        return "*"

    if field_display is None:
        field_display = fields

    alias_str = ""
    for field, alias in zip(fields, field_display):
        alias_str += f"{field} AS '{alias}', "
    return alias_str[:-2]


def get_filters(view_filter: str | None) -> str:
    """
    Construit la clause WHERE de la requête SQL en fonction du filtre de la vue.

    Args:
        view_filter (str | None): Filtre de la vue.

    Returns:
        str: Clause WHERE de la requête SQL.
    """
    if view_filter is None:
        return ""
    return f"WHERE {view_filter}"


class BaseView:
    """
    Classe de base pour les vues.

    Attributes:
        view_name (str): Nom de la vue.
        name_display (str): Nom de la vue à afficher.
        fields_name (List): Liste des noms de champ de la vue.
        fields_name_display (List): Liste des noms d'alias pour les champs à afficher.
        filter (str | None): Filtre à appliquer à la vue.
        default_order (str | None): Ordre par défaut des résultats.
        context_requirements (List | None): Exigences contextuelles.
        optional_context_requirements (List | None): Exigences contextuelles optionnelles.
        view_authorization (List): Autorisations nécessaires pour voir la vue.
        select_authorization (List): Autorisations nécessaires pour sélectionner des éléments de la vue.
        update_authorization (List): Autorisations nécessaires pour mettre à jour des éléments de la vue.
        delete_authorization (List): Autorisations nécessaires pour supprimer des éléments de la vue.
    """

    view_name = None
    name_display = None

    fields_name = None
    fields_name_display = None

    filter = None
    default_order = None

    context_requirements = None
    optional_context_requirements = None

    view_authorization = [authorization.IsCollaborator]
    select_authorization = [authorization.IsGestion]
    update_authorization = [authorization.IsGestion]
    delete_authorization = [authorization.Forbidden]

    @classmethod
    def is_user_authorize_to_view(cls, user: Collaborator) -> bool:
        """
        Vérifie si l'utilisateur a l'autorisation de voir la vue.

        Args:
            user (Collaborator): Utilisateur à vérifier.

        Returns:
            bool: True si l'utilisateur a l'autorisation, sinon False.
        """
        for auth in cls.view_authorization:
            if not auth.has_authorization(user):
                return False
        return True

    @classmethod
    def is_user_authorize_to_select(cls, user: Collaborator) -> bool:
        """
        Vérifie si l'utilisateur a l'autorisation de sélectionner des éléments de la vue.

        Args:
            user (Collaborator): Utilisateur à vérifier.

        Returns:
            bool: True si l'utilisateur a l'autorisation, sinon False.
        """
        for auth in cls.select_authorization:
            if not auth.has_authorization(user):
                return False
        return True

    @classmethod
    def is_user_authorize_to_delete(cls, user: Collaborator) -> bool:
        """
        Vérifie si l'utilisateur a l'autorisation de supprimer des éléments de la vue.

        Args:
            user (Collaborator): Utilisateur à vérifier.

        Returns:
            bool: True si l'utilisateur a l'autorisation, sinon False.
        """
        for auth in cls.delete_authorization:
            if not auth.has_authorization(user):
                return False
        return True

    @classmethod
    def has_requirements(cls) -> bool:
        """
        Vérifie si la vue a des exigences contextuelles.

        Returns:
            bool: True si la vue a des exigences, sinon False.
        """
        return cls.context_requirements is not None

    @classmethod
    def are_requirements_meet(cls, context: Context) -> bool:
        """
        Vérifie si les exigences contextuelles sont satisfaites.

        Args:
            context (Context): Contexte actuel.

        Returns:
            bool: True si les exigences sont satisfaites, sinon False.
        """
        if cls.context_requirements is None:
            return True
        for requirement in cls.context_requirements:
            if isinstance(requirement, str):
                return context.get_in_context(requirement) is not None

            if issubclass(requirement, BaseView):
                return (
                    context.current_view == requirement or context.current_view == cls
                )
        return True

    @classmethod
    def can_display(cls, context: Context) -> bool:
        """
        Vérifie si la vue peut être affichée dans le contexte actuel.

        Args:
            context (Context): Contexte actuel.

        Returns:
            bool: True si la vue peut être affichée, sinon False.
        """
        if not cls.is_user_authorize_to_view(context.current_user):
            return False
        if not cls.are_requirements_meet(context):
            return False
        return True

    @classmethod
    def get_query(cls) -> Tuple[str, Tuple]:
        """
        Retourne la requête SQL pour la vue.

        Returns:
            Tuple[str, Tuple]: Requête SQL et paramètres.
        """
        return (
            f"""
        SELECT {set_table_allias(cls.fields_name, cls.fields_name_display)} 
        FROM {cls.view_name} 
        {get_filters(cls.filter) if cls.filter is not None else ''}; 
        """,
            (),
        )


class CreateView(BaseView):
    form = None
    model = None
