from base.connector import get_connect
from base.context import Context
from base.display.rich_cli_display import RichQuestionaryCliDisplay as Display
from base.logger import logging
from epic_event_CRM.main_controller import EpicEventController

connector = get_connect("epicevent")
main_controller = EpicEventController()
display = Display()
context = Context(connector, display)

run = True
while run:
    try:
        main_controller.update_state(context)
        display.update(context)

        if (
            context.last_user_input == "Quit" or context.last_user_input is None
        ):  # None est un ctrl+C interupt
            run = False
            break

        main_controller.handle_user_input(context)

    except Exception as unhandled_error:
        logging.error(f" Erreur non gérée : {str(unhandled_error)}")
        error_message = "Une erreur non gérée s'est produite. Veuillez réessayer ou contacter le support."
        display.show_error(error_message)
        context.clear()  # On reset le context pour repartir sur le menu principal
