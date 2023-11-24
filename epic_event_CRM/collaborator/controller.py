from base.controller import BaseController
from epic_event_CRM.collaborator.form import CollaboratorCreationForm
from epic_event_CRM.collaborator.model import Collaborator
from epic_event_CRM.collaborator.serializer import CollaboratorSerializer
from epic_event_CRM.collaborator.view import CollaboratorView, CreateCollaboratorView


class CollaboratorController(BaseController):
    views = [CollaboratorView, CreateCollaboratorView]
    serializers = CollaboratorSerializer

    table = "collaborator"
    model = Collaborator
    form = CollaboratorCreationForm

    @classmethod
    def save(
        cls, python_object: Collaborator, connector, to_save=None, check_connection=True
    ):
        if python_object.id == -1:
            python_object.set_password()

            mysql_user_creation = f"CREATE USER {python_object.username}@'{connector.default_host}' IDENTIFIED BY %s;"
            connector.execute_query_w_val(
                mysql_user_creation, (python_object.password,)
            )

            mysql_role_granting = "CALL AssignRoleToCollaborator(%s, %s);"
            val_role_granting = (
                f"{python_object.username}@{connector.default_host}",
                f"{python_object.department.lower()}",
            )
            connector.execute_query_w_val(
                query=mysql_role_granting, val=val_role_granting
            )
        super().save(python_object, connector, to_save, check_connection)
