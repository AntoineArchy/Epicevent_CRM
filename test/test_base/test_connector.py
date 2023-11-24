import getpass

import pytest
from unittest.mock import MagicMock, patch

from _mysql_connector import MySQLError
from base.connector import (
    get_query_result,
    create_server_connection,
    execute_query_w_val,
    Connector,
    execute_list_query,
    construct_val_name_for_query,
    construct_col_name_for_query,
    construct_col_name_for_update,
    construct_val_for_update,
    get_user_login,
    log_ok_query,
    log_ko_query,
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
    result = get_query_result(
        query, include_fields=True, connection=connector.current_connection
    )

    # Vérifie que les résultats sont corrects
    assert result == [["Field1", "Field2"], ("Value1",), ("Value2",)]


def test_get_query_result_with_fields():
    # Teste la fonction get_query_result avec inclusion des noms de colonnes
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.description = [("Column1",), ("Column2",)]
    mock_cursor.fetchall.return_value = [(1, "value1"), (2, "value2")]
    mock_connection.cursor.return_value = mock_cursor

    query = "SELECT * FROM your_table"
    result = get_query_result(query, include_fields=True, connection=mock_connection)

    assert result == [["Column1", "Column2"], (1, "value1"), (2, "value2")]


def test_get_query_result_without_fields():
    # Teste la fonction get_query_result sans inclusion des noms de colonnes
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "value1"), (2, "value2")]
    mock_connection.cursor.return_value = mock_cursor

    query = "SELECT * FROM your_table"
    result = get_query_result(query, include_fields=False, connection=mock_connection)

    assert result == [(1, "value1"), (2, "value2")]


def test_get_query_result_empty_result():
    # Teste la fonction get_query_result avec un résultat vide
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection.cursor.return_value = mock_cursor

    query = "SELECT * FROM your_table"
    result = get_query_result(query, include_fields=True, connection=mock_connection)

    assert result == [[]]


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


def test_get_user_login_with_inputs(monkeypatch):
    # Simule l'entrée utilisateur pour les tests
    monkeypatch.setattr("builtins.input", lambda _: "test_username")
    monkeypatch.setattr(getpass, "getpass", lambda _: "test_password")

    result = get_user_login()

    assert result == ("test_username", "test_password")


def test_get_user_login_with_parameters():
    # Teste la fonction avec des paramètres fournis
    result = get_user_login(username="test_username", password="test_password")

    assert result == ("test_username", "test_password")


def test_create_server_connection_successful():
    # Teste la fonction lorsque la connexion à la base de données est réussie
    with patch("mysql.connector.connect", return_value=MagicMock()) as mock_connector:
        result = create_server_connection(
            "test_host", "test_user", "test_password", "test_database"
        )

    assert mock_connector.called
    assert result is not None


def test_create_server_connection_failure():
    # Teste la fonction lorsque la connexion à la base de données échoue
    with patch("mysql.connector.connect", side_effect=Exception("Connection failed")):
        try:
            create_server_connection(
                "test_host", "test_user", "test_password", "test_database"
            )
        except Exception as e:
            assert str(e) == "Connection failed"


def test_log_ok_query_with_value():
    # Teste la fonction avec une valeur
    with patch("logging.info") as mock_logging:
        log_ok_query("SELECT * FROM your_table", user="test_user", val="test_value")

    assert mock_logging.called_with(
        "User ID test_user: Query executed successfully: 'SELECT * FROM your_table' with value 'test_value'"
    )


def test_log_ok_query_without_value():
    # Teste la fonction sans valeur
    with patch("logging.info") as mock_logging:
        log_ok_query("SELECT * FROM your_table", user="test_user")

    assert mock_logging.called_with(
        "User ID test_user: Query executed successfully: 'SELECT * FROM your_table'"
    )


def test_log_ko_query_with_value_and_error():
    # Teste la fonction avec une valeur et un message d'erreur
    with patch("logging.error") as mock_logging:
        log_ko_query(
            "SELECT * FROM your_table",
            user="test_user",
            val="test_value",
            error="Query failed",
        )

    assert mock_logging.called_with(
        "User ID test_user: Error executing query 'SELECT * FROM your_table' with value 'test_value'. \n CAUSE :Query failed"
    )


def test_log_ko_query_without_value_and_error():
    # Teste la fonction sans valeur et sans message d'erreur
    with patch("logging.error") as mock_logging:
        log_ko_query("SELECT * FROM your_table", user="test_user", error="Query failed")

    assert mock_logging.called_with(
        "User ID test_user: Error executing query 'SELECT * FROM your_table'. \n CAUSE : Query failed"
    )
