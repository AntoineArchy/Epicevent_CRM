from base.controller import BaseController
from epic_event_CRM.client.form import ClientCreationForm
from epic_event_CRM.client.model import Client
from epic_event_CRM.client.serializer import ClientSerializer
from epic_event_CRM.client.view import (
    ClientView,
    UserOwnClientView,
    CreateClientView,
)


class ClientController(BaseController):
    views = [ClientView, UserOwnClientView, CreateClientView]
    serializers = ClientSerializer

    table = "client"
    model = Client
    form = ClientCreationForm
