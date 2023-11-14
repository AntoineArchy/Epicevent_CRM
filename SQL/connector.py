import logging
from typing import Tuple, Dict, List

import mysql.connector
from mysql.connector import Error
import getpass

from epic_event_CRM.collaborator.model import Collaborator


def construct_col_name_for_update(obj_dict: Dict) -> str:
    col_name_alias = ""
    for key in obj_dict.keys():
        col_name_alias += f"{key} = %s, "
    col_name_alias = col_name_alias[:-2]
    return col_name_alias


def construct_val_for_update(obj_dict: Dict) -> List:
    return list(map(str, obj_dict.values()))


def construct_col_name_for_query(obj_dict: Dict) -> str:
    return f"{tuple([*obj_dict.keys()])}".replace("'", "")


def construct_val_name_for_query(obj_dict: Dict) -> Tuple:
    return tuple([*obj_dict.values()])


def do_query(query, include_fields, connection=None):
    if connection is None:
        return None

    results = list()

    cursor = connection.cursor()
    cursor.execute(f"{query}")
    if include_fields:
        results.append([i[0] for i in cursor.description])
    results.extend(cursor.fetchall())

    return results


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password
        )
        logging.info("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query_w_val(connection, query, val):
    cursor = connection.cursor()
    try:
        cursor.execute(query, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_list_query(connection, sql):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def get_user_login(username=None, password=None) -> Tuple:
    if username is None:
        username = input("username ? ")

    if password is None:
        password = getpass.getpass("Whats your password?")

    return username, password


class Connector:
    def __init__(self, username: str = None, password: str = None):
        if username is None or password is None:
            username, password = get_user_login(username, password)

        self.current_user = username
        self.current_connection = create_server_connection(
            "localhost", username, password
        )

        if self.current_connection is None:
            return

        execute_query(self.current_connection, "USE epicevent")
        user_data = do_query(
            f"SELECT * from collaborator where username = '{username}'",
            True,
            self.current_connection,
        )
        self.current_user = Collaborator(**dict(zip(*user_data)))

    def do_query(self, query, include_fields):
        return do_query(query, include_fields, self.current_connection)

    def execute_query(self, query):
        return execute_query(self.current_connection, query)

    def execute_query_w_val(self, query, val):
        return execute_query_w_val(self.current_connection, query, val)

    def create(self, table, obj_dict):
        query = f"""INSERT INTO {table} {construct_col_name_for_query(obj_dict)} 
                            VALUES (%s{', %s' * (len(obj_dict) -1)})"""
        values = construct_val_name_for_query(obj_dict)

        self.execute_query_w_val(query, values)

    def update(self, table, obj_dict, id):
        query = f"""UPDATE {table} SET {construct_col_name_for_update(obj_dict)} 
                                            WHERE {table}_id = %s
                                """
        val = construct_val_for_update(obj_dict)
        val.append(str(id))
        self.execute_query_w_val(query, val)

    def read(self, query, include_fields):
        results = self.do_query(query=query, include_fields=include_fields)
        return results

    def delete(self):
        pass


# connector = Connector()
