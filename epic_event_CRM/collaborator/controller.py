from epic_event_CRM.base.controller import BaseController
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
    def save(cls, python_object: Collaborator, connector):
        if python_object.id == -1:
            mysql_user_creation = f"""
            CREATE USER {python_object.username}@'localhost' IDENTIFIED BY '{python_object.password}';
            """

            mysql_role_granting = f"""
            GRANT '{python_object.department.lower()}' TO '{python_object.username}'@'localhost';
            """

            connector.execute_query(query=mysql_user_creation)
            connector.execute_query(query=mysql_role_granting)
        super().save(python_object, connector)
