from typing import List


class Context:
    def __init__(self, connector, display):
        """
        Initialise un objet Context pour gérer le contexte de l'application.

        Args:
            connector: Objet Connector pour la connexion à la base de données.
            display: Objet pour l'affichage des résultats.
        """
        self.current_connector = connector
        self.display = display
        self.current_user = connector.current_user

        self.current_view = None
        self.data_to_display = {"fields": None, "data": None}
        self.last_user_input = None
        self.current_available_option = None

        self.in_context = dict()

    def get_data_length(self):
        """
        Renvoie la longueur des données actuellement affichées.

        Returns:
            int: Longueur des données.
        """
        if self.data_to_display.get("data", None) is None:
            return 0
        return len(self.data_to_display["data"])

    def clear(self):
        """
        Efface le contexte actuel.
        """
        self.current_view = None
        self.data_to_display = {"fields": None, "data": None}
        self.last_user_input = None
        self.current_available_option = None

        self.in_context = dict()

    def set_in_context(self, name, obj):
        """
        Stocke un objet dans le contexte.

        Args:
            name (str): Nom de l'objet dans le contexte.
            obj: Objet à stocker.
        """
        self.in_context[name] = obj

    def get_in_context(self, context_object):
        """
        Récupère un objet du contexte.

        Args:
            context_object (str): Nom de l'objet à récupérer.

        Returns:
            obj: Objet du contexte.
        """
        return self.in_context.get(context_object, None)

    def get_user_choice(self):
        """
        Récupère le choix de l'utilisateur parmi les options disponibles.

        Returns:
            Tuple: Tuple contenant le choix de l'utilisateur.
        """
        for available_option in self.current_available_option:
            if self.last_user_input == available_option[0]:
                return available_option
        return None, None

    def get_dynamic_menu(self):
        """
        Récupère le menu dynamique en fonction de la vue actuelle.

        Returns:
            List: Liste des options du menu.
        """
        if self.current_view is not None:
            self.current_available_option.append(("Menu principal", None, None))

        menu_str = [option[0] for option in self.current_available_option]

        return menu_str

    def set_current_display(self, view=None, fields: List = None, data: List = None):
        """
        Définit la vue et les données actuelles à afficher.

        Args:
            view (str): Nom de la vue à afficher.
            fields (List): Liste des champs à afficher.
            data (List): Liste des données à afficher.
        """
        if view is not None:
            self.current_view = view

        if fields is not None:
            self.data_to_display["fields"] = fields

        if data is not None:
            self.data_to_display["data"] = data
