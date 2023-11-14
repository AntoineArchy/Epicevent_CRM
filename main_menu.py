from SQL.connector import Connector
from display.rich_cli_display import RichQuestionaryCliDisplay as Display
from epic_event_CRM.base.context import Context
from epic_event_CRM.controller import EpicEventController

connector = Connector()
main_controller = EpicEventController()
display = Display()
context = Context(connector, display)

run = True
while run:
    main_controller.update(context)
    display.update(context)

    if context.last_user_input == "Quit" or context.last_user_input is None:
        run = False
        break

    main_controller.handle_user_input(context)
