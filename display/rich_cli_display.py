import os

import questionary
from rich.console import Console
from rich.table import Table


def feed_table(view_name, results, as_select):
    table = Table(title=view_name)

    field_names = results["fields"]
    table_data = results["data"]

    if as_select:
        field_names = ["Selection Idx.", *field_names]

    for name in field_names:
        table.add_column(str(name))

    for elt_index, result in enumerate(table_data, start=0):
        if as_select:
            result = [elt_index, *result]
        str_results = [*map(str, result)]
        table.add_row(*str_results)
    return table


def get_table(view_name, results, as_select=False):
    table = feed_table(view_name, results, as_select)
    return table


def display_query_results(view_name, to_display, as_select=False):
    table = get_table(view_name, to_display, as_select)

    console = Console()
    console.print(table, justify="center")


class RichQuestionaryCliDisplay:
    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display_actual_view(view_name, data_to_display):
        display_query_results(view_name, data_to_display)

    @staticmethod
    def select_field_from_form(form):
        to_return_form = list()

        selected_fields = questionary.checkbox(
            "Sélectionnez les champs :",
            choices=form.fields_display,
        ).ask()
        if not selected_fields:
            return None

        indexes = [
            form.fields_display.index(field_name) for field_name in selected_fields
        ]
        for field_idx in indexes:
            to_return_form.append(form.questions[field_idx])
        return to_return_form

    @staticmethod
    def fill_form(form=None, form_data=None):
        if form_data is None:
            return questionary.prompt(form.questions)
        return questionary.prompt(form_data)

    @staticmethod
    def select_from_current_view(view_name, data_to_display):
        display_query_results(view_name, data_to_display, as_select=True)
        select_menu = questionary.select(
            "Selection n° : ",
            choices=[
                *[
                    str(selection_nbr)
                    for selection_nbr in range(len(data_to_display["data"]))
                ],
                "Back",
            ],
        )
        return select_menu.ask()

    @staticmethod
    def display_option_menu(dynamic_menu, message="What do you want to do?"):
        return questionary.select(
            message,
            choices=[*dynamic_menu, "Quit"],
        )

    def get_user_input(self, context):
        return self.display_option_menu(context.get_dynamic_menu()).ask()

    def update(self, context):
        self.clear()
        if context.current_view is not None:
            self.display_actual_view(
                context.current_view.name_display, context.data_to_display
            )
        context.last_user_input = self.get_user_input(context)
