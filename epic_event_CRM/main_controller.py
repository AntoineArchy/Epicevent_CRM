from base.controller import BaseController
from epic_event_CRM.client.controller import ClientController
from epic_event_CRM.collaborator.controller import CollaboratorController
from epic_event_CRM.contract.controller import ContractController
from epic_event_CRM.event.controller import EventController


class EpicEventController(BaseController):
    """
    Contrôleur principal de l'application Epic Event.

    Attributes:
        controllers (List): Liste des contrôleurs spécifiques à chaque entité de l'application.
    """

    controllers = [
        ClientController,
        ContractController,
        EventController,
        CollaboratorController,
    ]

    def get_allowed_views(self, context):
        """
        Récupère les vues autorisées pour le contexte actuel.

        Args:
            context (Context): Contexte actuel.

        Returns:
            List: Liste des vues autorisées.
        """
        dynamic_view_menu = list()

        for controller in self.controllers:
            dynamic_view_menu.extend(controller.get_allowed_views(context))
        return dynamic_view_menu

    def update_dynamic_menu(self, context):
        """
        Met à jour le menu dynamique en fonction des vues autorisées dans le contexte.

        Args:
            context (Context): Contexte actuel.
        """
        allowed_user_input = self.get_allowed_views(context)

        context.current_available_option = allowed_user_input

    @classmethod
    def handle_user_input(cls, context, _=None):
        """
        Gère l'input utilisateur pour sélectionner une vue spécifique et le dispatch au bon controller.

        Args:
            context (Context): Contexte actuel.
            _ : Ignoré (Ajouté pour coller a la signature de la fonction parent).
        """
        user_str_choice, chosen_view, adequate_controller = context.get_user_choice()

        if user_str_choice is None or adequate_controller is None:
            context.clear()
            return

        adequate_controller.handle_user_input(context, chosen_view)

    def update_state(self, context):
        """
        Met à jour l'état du contrôleur en mettant à jour le menu dynamique.

        Args:
            context (Context): Contexte actuel.
        """
        self.update_dynamic_menu(context)
