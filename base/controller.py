from __future__ import annotations

import datetime
import re
from typing import List, Dict

from base.connector import Connector
from base.form import BaseForm
from base.model import BaseModel
from base.serializer import BaseSerializer
from base.view import BaseView, CreateView
from base.context import Context


def sanitize_input(input_str):
    """
    Supprime les caractères spéciaux d'une chaîne de caractères.

    Args:
        input_str (str): Chaîne de caractères à nettoyer.

    Returns:
        str: Chaîne de caractères nettoyée.
    """
    words = input_str.split()
    sanitized_words = [re.sub(r"[^a-zA-Z0-9À-ÿ\s]", "", word) for word in words]
    sanitized_input = " ".join(sanitized_words)
    return sanitized_input


class BaseController:
    views = [BaseView, CreateView]
    serializers = BaseSerializer

    table = None

    model = BaseModel
    form = BaseForm

    @classmethod
    def fill_obj_form(cls, context):
        """
        Remplit le formulaire d'un objet.

        Args:
            context (Context): Objet contexte.

        Returns:
            dict: Formulaire rempli.
        """
        filled_form = context.display.fill_form(cls.form)
        return filled_form

    @classmethod
    def create(cls, context: Context, form: Dict = None) -> BaseModel:
        """
        Crée un nouvel objet à partir du formulaire.

        Args:
            context (Context): Objet contexte.
            form (Dict): Formulaire à utiliser (optionnel).

        Returns:
            BaseModel: Nouvel objet créé.
        """
        if form is None:
            form = cls.fill_obj_form(context)
        created_obj = cls.model(**form)
        return created_obj

    @classmethod
    def update(
        cls,
        fields_to_update: Dict,
        context: Context,
        obj_to_update: BaseModel | None = None,
    ) -> None:
        """
        Met à jour un objet avec de nouveaux champs.

        Args:
            fields_to_update (Dict): Champs à mettre à jour.
            context (Context): Objet contexte.
            obj_to_update (BaseModel | None): Objet à mettre à jour (optionnel).
        """
        if obj_to_update is None:
            obj_to_update = context.get_in_context(cls.table)
        fields_to_update["last_update"] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        cls.save(
            python_object=obj_to_update,
            connector=context.current_connector,
            to_save=fields_to_update,
        )
        context.clear()

    @classmethod
    def set_to_display(
        cls, context: Context, fields: List = None, data: List = None
    ) -> None:
        """
        Configure l'affichage dans le contexte.

        Args:
            context (Context): Objet contexte.
            fields (List): Liste des champs à afficher (optionnel).
            data (List): Liste des données à afficher (optionnel).
        """
        context.set_current_display(fields=fields, data=data)

    @classmethod
    def save(
        cls,
        python_object: BaseModel,
        connector: Connector,
        to_save=None,
        check_connection=True,
    ) -> None:
        """
        Sauvegarde un objet dans la base de données.

        Args:
            python_object (BaseModel): Objet à sauvegarder.
            connector (Connector): Connecteur à la base de données.
            to_save: Champs à sauvegarder (optionnel).
            check_connection (bool): Vérifier la connexion avant de sauvegarder (optionnel).
        """
        if check_connection:
            connector.reset_connection()
        if to_save is None:
            to_save = python_object.__dict__
        obj_id = python_object.__dict__.get(python_object.id_name)

        if obj_id == -1:
            to_save.pop(python_object.id_name)
            connector.create(cls.table, to_save)
            return
        connector.update(cls.table, to_save, obj_id)
        return

    @classmethod
    def get_context_related_view(cls, context: Context) -> List:
        """
        Obtient les vues liées au contexte.

        Args:
            context (Context): Objet contexte.

        Returns:
            List: Liste des vues autorisées.
        """
        allowed = list()

        for view in cls.views:
            if not view.can_display(context):
                continue

            if not view.has_requirements():
                continue
            allowed.append((f"{view.name_display}", view, cls))

        return allowed

    @classmethod
    def get_allowed_views(cls, context: Context) -> List:
        """
        Obtient les vues autorisées dans le contexte.

        Args:
            context (Context): Objet contexte.

        Returns:
            List: Liste des vues autorisées.
        """
        if context.current_view is not None and context.current_view not in cls.views:
            return cls.get_context_related_view(context)

        allowed = list()
        for view in cls.views:
            if not view.can_display(context):
                continue

            if context.current_view != view:
                allowed.append((f"{view.name_display}", view, cls))
                continue

            if context.get_data_length() == 0:
                continue

            if view.is_user_authorize_to_select(context.current_user):
                if context.get_in_context(cls.table) is not None:
                    if view.is_user_authorize_to_delete(context.current_user):
                        allowed.append((f"Désactivé", view, cls))
                    allowed.append((f"Mettre à jour", view, cls))
                    continue
                allowed.append((f"Selection", view, cls))
                continue

        return allowed

    @classmethod
    def return_view_selection(
        cls, context: Context, chosen_view: BaseView
    ) -> BaseModel:
        """
        Récupère la sélection faite depuis une vue.

        Args:
            context (Context): Objet contexte.
            chosen_view (BaseView): Vue choisie.

        Returns:
            BaseModel: Objet sélectionné.
        """
        selected_idx = context.display.select_from_current_view(
            chosen_view.name_display, data_to_display=context.data_to_display
        )
        if selected_idx is None or selected_idx.lower() == "back":
            return None

        selected_in_list = dict(
            zip(
                context.data_to_display["fields"],
                context.data_to_display["data"][int(selected_idx)],
            )
        )
        form = cls.serializers.from_view_data_to_obj_dict(selected_in_list)
        selected_obj = cls.create(context, form=form)
        return selected_obj

    @classmethod
    def handle_user_select(cls, context, chosen_view):
        """
        Gère la sélection d'un objet'.

        Args:
            context (Context): Objet contexte.
            chosen_view (BaseView): Vue choisie.
        """
        if context.current_view == chosen_view:
            context.display.clear()
        else:
            cls.handle_user_read(context, chosen_view)

        selected_obj = cls.return_view_selection(context, chosen_view)
        if selected_obj is None:
            context.clear()
            return
        context.set_in_context(cls.table, selected_obj)
        obj_display = cls.serializers.from_obj_to_view_data(selected_obj)
        context.set_current_display(
            fields=obj_display.keys(), data=[obj_display.values()]
        )
        return selected_obj

    @classmethod
    def get_answer(cls, context, question):
        """
        Obtient la réponse de l'utilisateur à une question.

        Args:
            context (Context): Objet contexte.
            question: Question posée.

        Returns:
            dict: Réponses de l'utilisateur.
        """
        user_answer = context.display.fill_form(form_data=question)
        sanitized_input = dict()
        for field_name, user_input in user_answer.items():
            sanitized_input[field_name] = sanitize_input(user_input)
        return sanitized_input

    @classmethod
    def handle_user_update(cls, context):
        """
        Gère la mise à jour d'un objet par l'utilisateur.

        Args:
            context (Context): Objet contexte.
        """
        form_fields = cls.form.get_fields(context)
        fields_to_update = context.display.select_field_from_form(form_fields)
        if fields_to_update is None:
            return

        updated_fields = dict()
        for field_name in fields_to_update:
            question = cls.form.get_question(field_name)
            answer = cls.get_answer(context, question)
            if answer is not None:
                updated_fields.update(answer)

        cls.update(fields_to_update=updated_fields, context=context)

    @classmethod
    def handle_user_create(cls, context, chosen_view):
        """
        Gère la création d'un objet par l'utilisateur.

        Args:
            context (Context): Objet contexte.
            chosen_view (BaseView): Vue choisie.
        """
        obj = cls.create(context)
        if obj is None:
            context.display.show_error("Impossible de Poursuivre la création.")
            return
        cls.save(obj, context.current_connector)

        obj.set_id(context.current_connector.get_last_inserted_id())
        obj_display = cls.serializers.from_obj_dict_to_view_data(obj.__dict__)
        context.set_current_display(
            view=chosen_view, fields=obj_display.keys(), data=[obj_display.values()]
        )
        context.set_in_context(cls.table, obj)

    @classmethod
    def handle_user_delete(cls, context):
        """
        Gère la suppression d'un objet par l'utilisateur.

        Args:
            context (Context): Objet contexte.
        """
        conf = None
        while conf not in ["o", "n"]:
            conf = input("Êtes vous sur ? O/N").lower()

        if conf == "n":
            context.clear()
            return
        field_to_update = {"is_active": 0}
        cls.update(field_to_update, context)

    @classmethod
    def handle_user_read(cls, context, chosen_view):
        """
        Gère la lecture d'une vue par l'utilisateur.

        Args:
            context (Context): Objet contexte.
            chosen_view (BaseView): Vue choisie.
        """
        query, val = chosen_view.get_query()
        results = context.current_connector.read(query, val, include_fields=True)

        context.set_current_display(
            view=chosen_view, fields=results.pop(0), data=results
        )

    @classmethod
    def handle_user_input(cls, context: Context, chosen_view: BaseView) -> None:
        """
        Dispatch le choix de l'utilisateur à la fonction adaptée.

        Args:
            context (Context): Objet contexte.
            chosen_view (BaseView): Vue choisie.
        """
        user_str_choice = context.last_user_input
        if user_str_choice.lower() == "selection":
            cls.handle_user_select(context, chosen_view)
            return

        elif user_str_choice.lower() == "mettre à jour":
            cls.handle_user_update(context)
            return

        elif user_str_choice.lower() == "désactivé":
            cls.handle_user_delete(context)
            return

        elif issubclass(chosen_view, CreateView):
            cls.handle_user_create(context, chosen_view)
            return

        elif issubclass(chosen_view, BaseView):
            cls.handle_user_read(context, chosen_view)
            return
