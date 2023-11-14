from epic_event_CRM.base.controller import BaseController
from epic_event_CRM.base.view import BaseView
from epic_event_CRM.client.controller import ClientController
from epic_event_CRM.collaborator.controller import CollaboratorController
from epic_event_CRM.contract.controller import ContractController
from epic_event_CRM.event.controller import EventController


class EpicEventController(BaseController):
    controllers = [
        ClientController,
        ContractController,
        EventController,
        CollaboratorController,
    ]

    def get_allowed_views(self, context):
        dynamic_view_menu = list()

        for controller in self.controllers:
            dynamic_view_menu.extend(controller.get_allowed_views(context))
        return dynamic_view_menu

    def update_dynamic_menu(self, context):
        allowed_user_input = self.get_allowed_views(context)

        context.current_available_option = allowed_user_input

    @classmethod
    def handle_user_input(cls, context, _=None):
        user_str_choice, chosen_view, adequate_controller = context.get_user_choice()

        if user_str_choice is None or adequate_controller is None:
            context.clear()
            return

        adequate_controller.handle_user_input(context, chosen_view)

    def update(self, context):
        self.update_dynamic_menu(context)
