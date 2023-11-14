from typing import List


class Context:
    def __init__(self, connector, display):
        self.current_connector = connector
        self.display = display
        self.current_user = connector.current_user

        self.current_view = None
        self.data_to_display = {"fields": None, "data": None}
        self.last_user_input = None
        self.current_available_option = None

        self.in_context = dict()

    def clear(self):
        self.current_view = None
        self.data_to_display = {"fields": None, "data": None}
        self.last_user_input = None
        self.current_available_option = None

        self.in_context = dict()

    def set_in_context(self, name, obj):
        self.in_context[name] = obj

    def get_in_context(self, args):
        to_return = None
        if args in self.in_context:
            to_return = self.in_context.get(args)
        return to_return

    def get_user_choice(self):
        for available_option in self.current_available_option:
            if self.last_user_input == available_option[0]:
                return available_option
        return None, None

    def get_dynamic_menu(self):
        if self.current_view is not None:
            self.current_available_option.append(("Menu principal", None, None))

        menu_str = [option[0] for option in self.current_available_option]

        return menu_str

    def set_current_display(self, view=None, fields: List = None, data: List = None):
        if view is not None:
            self.current_view = view

        if fields is not None:
            self.data_to_display["fields"] = fields

        if data is not None:
            self.data_to_display["data"] = data
