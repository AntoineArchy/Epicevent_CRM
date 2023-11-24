import os

import questionary
from rich.console import Console
from rich.table import Table


def feed_table(table, results, as_select):
    """
    Ajoute des donnée dans une table Rich.

    Args:
        table (rich.table.Table): La table Rich à laquelle ajouter les résultats.
        results (dict): Les résultats de la requête.
        as_select (bool): Indique si la table est utilisée pour une sélection.

    Returns:
        rich.table.Table: La table mise à jour.
    """
    table_data = results["data"]

    for elt_index, result in enumerate(table_data, start=0):
        if as_select:
            result = [elt_index, *result]
        str_results = [*map(str, result)]
        table.add_row(*str_results)
    return table


def get_table(view_name, results, as_select=False):
    """
    Crée une table Rich à partir des résultats de la requête.

    Args:
        view_name (str): Le nom de la vue.
        results (dict): Les résultats de la requête.
        as_select (bool): Indique si la table est utilisée pour une sélection.

    Returns:
        rich.table.Table: La table créée.
    """
    if results["data"] is None or len(results["data"]) == 0:
        return f"{view_name} \n No data to display"
    table = Table(title=view_name)

    field_names = results["fields"]

    if as_select:
        field_names = ["Selection Idx.", *field_names]

    for name in field_names:
        table.add_column(str(name))
    feed_table(table, results, as_select)
    return table


def display_query_results(view_name, to_display, as_select=False):
    """
    Affiche les résultats de la requête dans la console.

    Args:
        view_name (str): Le nom de la vue.
        to_display (dict): Les résultats de la requête.
        as_select (bool): Indique si la table est utilisée pour une sélection.
    """
    table = get_table(view_name, to_display, as_select)

    console = Console()
    console.print(table, justify="center")


class RichQuestionaryCliDisplay:
    @staticmethod
    def show_error(message):
        """
        Affiche les résultats de la requête dans la console.

        Args:
            view_name (str): Le nom de la vue.
            to_display (dict): Les résultats de la requête.
            as_select (bool): Indique si la table est utilisée pour une sélection.
        """
        console = Console()
        console.print(f"[bold red]Erreur : {message}[/bold red]")

    @staticmethod
    def clear():
        """Efface l'écran de la console."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display_actual_view(view_name, data_to_display):
        """
        Affiche la vue actuelle dans la console.

        Args:
            view_name (str): Le nom de la vue.
            data_to_display (dict): Les données à afficher.
        """
        display_query_results(view_name, data_to_display)

    @staticmethod
    def select_field_from_form(form):
        """
        Permet à l'utilisateur de sélectionner des champs dans un formulaire.

        Args:
            form (list): La liste des champs à sélectionner.

        Returns:
            list or None: Les champs sélectionnés ou None si aucun champ n'est sélectionné.
        """
        selected_fields = questionary.checkbox(
            "Sélectionnez les champs :",
            choices=form,
        ).ask()
        if not selected_fields:
            return None
        return selected_fields

    @staticmethod
    def fill_form(form=None, form_data=None):
        """
        Remplit un formulaire.

        Args:
            form (list): La liste des questions du formulaire.
            form_data (dict): Les données pré-remplies du formulaire.

        Returns:
            dict: Les réponses du formulaire."""
        if form_data is None:
            return questionary.prompt(form.questions)
        return questionary.prompt(form_data)

    @staticmethod
    def select_from_current_view(view_name, data_to_display):
        """
        Permet à l'utilisateur de sélectionner une entrée dans la vue actuelle.

        Args:
            view_name (str): Le nom de la vue.
            data_to_display (dict): Les données à afficher.

        Returns:
            str: L'index de l'entrée sélectionnée ou "Back" pour revenir en arrière.
        """
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
    def display_option_menu(dynamic_menu, message="Que voulez-vous faire ?"):
        """
        Affiche un menu d'options dans la console.

        Args:
            dynamic_menu (list): La liste des options du menu.
            message (str): Le message du menu.

        Returns:
            str: L'option sélectionnée.
        """
        return questionary.select(
            message,
            choices=[*dynamic_menu, "Quit"],
        )

    def get_user_input(self, context):
        """
        Affiche un menu d'options dans la console.

        Args:
            dynamic_menu (list): La liste des options du menu.
            message (str): Le message du menu.

        Returns:
            str: L'option sélectionnée.
        """
        return self.display_option_menu(context.get_dynamic_menu()).ask()

    def update(self, context):
        """
        Met à jour l'écran en affichant la vue actuelle et en récupérant l'entrée de l'utilisateur.

        Args:
            context (object): Le contexte de l'application.
        """
        self.clear()
        if context.current_view is not None:
            self.display_actual_view(
                context.current_view.name_display, context.data_to_display
            )
        context.last_user_input = self.get_user_input(context)
