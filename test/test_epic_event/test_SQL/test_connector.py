from getpass import getpass

import pytest
from unittest.mock import MagicMock

from _mysql_connector import MySQLError
from mysql.connector.errors import Error
from SQL.connector import (
    do_query,
    create_server_connection,
    execute_query,
    execute_query_w_val,
    Connector,
    execute_list_query,
    construct_val_name_for_query,
    construct_col_name_for_query,
    construct_col_name_for_update,
    construct_val_for_update,
)


def test_construct_col_name_for_query():
    obj_data = {"field1": "value1", "field2": "value2"}
    result = construct_col_name_for_query(obj_data)
    assert result == "(field1, field2)"


def test_construct_col_name_for_update():
    obj_data = {"field1": "value1", "field2": "value2"}
    result = construct_col_name_for_update(obj_data)
    assert result == "field1 = %s, field2 = %s"


def test_construct_val_for_update():
    obj_data = {"field1": "value1", "field2": "value2"}
    result = construct_val_for_update(obj_data)
    assert result == ["value1", "value2"]


def test_construct_val_name_for_query():
    obj_data = {"field1": "value1", "field2": "value2"}
    result = construct_val_name_for_query(obj_data)
    assert result == ("value1", "value2")


def test_do_query():
    # Crée un mock pour le connecteur actuel
    connector = MagicMock()
    connector.current_connection.cursor().description = [("Field1",), ("Field2",)]
    connector.current_connection.cursor().fetchall.return_value = [
        ("Value1",),
        ("Value2",),
    ]

    # Définit une requête SQL
    query = "SELECT * FROM my_table"

    # Appelle la fonction do_query
    result = do_query(
        query, include_fields=True, connection=connector.current_connection
    )

    # Vérifie que les résultats sont corrects
    assert result == [["Field1", "Field2"], ("Value1",), ("Value2",)]


def test_create_server_connection_failure():
    # Définit les paramètres de connexion incorrects
    host_name = "localhost"
    user_name = "test_user"
    user_password = "wrong_password"

    # Appelle la fonction create_server_connection
    result = create_server_connection(host_name, user_name, user_password)

    # Vérifie que la connexion a échoué
    assert result is None


def test_execute_query_successful():
    # Crée un mock pour le connecteur actuel
    connector = MagicMock()

    # Définit une requête SQL
    query = "INSERT INTO my_table (Field1, Field2) VALUES ('Value1', 'Value2')"

    # Appelle la fonction execute_query
    execute_query(connector.current_connection, query)

    # Vérifie que la requête a été exécutée avec succès
    connector.current_connection.cursor().execute.assert_called_once_with(query)


def execute_query_failure():
    # Crée un mock pour le connecteur actuel avec une erreur simulée
    connector = MagicMock()
    connector.current_connection.cursor().execute.side_effect = MySQLError("Test error")

    # Définit une requête SQL
    query = "INSERT INTO my_table (Field1, Field2) VALUES ('Value1', 'Value2')"

    # Appelle la fonction execute_query et capture l'exception
    with pytest.raises(MySQLError):
        execute_query(connector.current_connection, query)


def test_execute_query_w_val_successful():
    # Crée un mock pour le connecteur actuel
    connector = MagicMock()

    # Définit une requête SQL et des valeurs
    query = "INSERT INTO my_table (Field1, Field2) VALUES (%s, %s)"
    val = ("Value1", "Value2")

    # Appelle la fonction execute_query_w_val
    execute_query_w_val(connector.current_connection, query, val)

    # Vérifie que la requête a été exécutée avec succès
    connector.current_connection.cursor().execute.assert_called_once_with(query, val)


def test_execute_query_w_val_failure():
    # Crée un mock pour le connecteur actuel avec une erreur simulée
    connector = MagicMock()
    connector.current_connection.cursor().execute.side_effect = MySQLError("Test error")

    # Définit une requête SQL et des valeurs
    query = "INSERT INTO my_table (Field1, Field2) VALUES (%s, %s)"
    val = ("Value1", "Value2")

    # Appelle la fonction execute_query_w_val et capture l'exception
    with pytest.raises(MySQLError):
        execute_query_w_val(connector.current_connection, query, val)


def test_execute_list_query_success():
    # Crée un mock pour la connexion
    connection = MagicMock()

    # Configure le mock pour réussir l'exécution de la requête
    connection.cursor().executemany.return_value = None

    # Définit la requête SQL
    sql = "INSERT INTO my_table (Field1, Field2) VALUES (%s, %s)"
    val = [("Value1", "Value2"), ("Value3", "Value4")]

    # Appelle la fonction execute_list_query
    execute_list_query(connection, sql)

    # Vérifie que la requête a été exécutée avec les valeurs fournies
    connection.cursor().executemany.assert_called_once_with(sql)


def test_execute_list_query_failure():
    # Crée un mock pour la connexion
    connection = MagicMock()

    # Configure le mock pour simuler une erreur lors de l'exécution de la requête
    connection.cursor().executemany.side_effect = MySQLError("Test error")

    # Définit la requête SQL
    sql = "INSERT INTO my_table (Field1, Field2) VALUES (%s, %s)"
    val = [("Value1", "Value2"), ("Value3", "Value4")]

    # Appelle la fonction execute_list_query et capture l'exception
    with pytest.raises(MySQLError):
        execute_list_query(connection, sql)


def test_connector_init_ko(monkeypatch):
    # Crée un mock pour le connecteur
    connector = Connector("test_user", "test_password")

    # Vérifie que le nom d'utilisateur actuel est correct
    assert connector.current_user == "test_user"
    # Vérifie que la connexion actuelle a été établie
    assert connector.current_connection is None
