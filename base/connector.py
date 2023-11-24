import logging
import sys
from typing import Tuple, Dict, List

import mysql.connector
from mysql.connector import Error
import getpass

from epic_event_CRM.collaborator.model import Collaborator

from utils import hash_password, get_host_default_from_config


def construct_col_name_for_update(obj_dict: Dict) -> str:
    """
    Construit la liste des colonnes pour une requête UPDATE.

    Args:
        obj_dict (Dict): Dictionnaire des colonnes et valeurs à mettre à jour.

    Returns:
        str: Chaîne des colonnes pour la requête UPDATE.
    """
    col_name_alias = ""
    for key in obj_dict.keys():
        col_name_alias += f"{key} = %s, "
    col_name_alias = col_name_alias[:-2]
    return col_name_alias


def construct_val_for_update(obj_dict: Dict) -> List:
    """
    Construit la liste des valeurs pour une requête UPDATE.

    Args:
        obj_dict (Dict): Dictionnaire des colonnes et valeurs à mettre à jour.

    Returns:
        List: Liste des valeurs pour la requête UPDATE.
    """
    return list(map(str, obj_dict.values()))


def construct_col_name_for_query(obj_dict: Dict) -> str:
    """
    Construit la liste des noms de colonnes pour une requête INSERT.

    Args:
        obj_dict (Dict): Dictionnaire des colonnes et valeurs à insérer.

    Returns:
        str: Chaîne des noms de colonnes pour la requête INSERT.
    """
    return f"{tuple([*obj_dict.keys()])}".replace("'", "")


def construct_val_name_for_query(obj_dict: Dict) -> Tuple:
    """
    Construit la liste des valeurs pour une requête INSERT.

    Args:
        obj_dict (Dict): Dictionnaire des colonnes et valeurs à insérer.

    Returns:
        Tuple: Tuple des valeurs pour la requête INSERT.
    """
    return tuple([*obj_dict.values()])


def get_query_result(query, val=None, include_fields=False, connection=None):
    """
    Exécute une requête SQL et récupère le résultat.

    Args:
        query (str): Requête SQL.
        include_fields (bool): Indique si les noms de colonnes doivent être inclus.
        connection: Connexion à la base de données.

    Returns:
        List: Résultat de la requête.
    """

    results = list()
    with connection.cursor() as cursor:
        cursor.execute(f"{query}", val)
        if include_fields:
            results.append([i[0] for i in cursor.description])
        results.extend(cursor.fetchall())
    return results


def execute_query_w_val(connection, query, val):
    """
    Exécute une requête SQL avec des valeurs.

    Args:
        connection: Connexion à la base de données.
        query (str): Requête SQL.
        val: Valeurs à utiliser dans la requête.

    Returns:
        bool: True si l'exécution réussit, sinon False.
    """
    with connection.cursor() as cursor:
        cursor.execute(query, val)
        connection.commit()
    return True


def execute_list_query(connection, sql):
    with connection.cursor() as cursor:
        cursor.executemany(sql)
        connection.commit()
    return True


def get_user_login(username=None, password=None, skip_hash=False) -> Tuple:
    if username is None:
        username = input("Nom d'utilisateur ? ")

    if password is None:
        password = getpass.getpass("Mot de passe ? ")

    if not skip_hash:
        password = hash_password(password)
    return username, password


def create_server_connection(host_name, user_name, user_password, database=None):
    """
    Crée une connexion à la base de données MySQL.

    Args:
        host_name (str): Nom de l'hôte.
        user_name (str): Nom d'utilisateur.
        user_password (str): Mot de passe de l'utilisateur.
        database (str): Nom de la base de données (optionnel).

    Returns:
        connection: Connexion à la base de données.
    """
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=database
        )
        logging.info("MySQL Database connection successful")
        return connection

    except Error as err:
        raise err


def log_ok_query(query, user, val=None):
    """
    Journalise le succès de l'exécution d'une requête.

    Args:
        query (str): Requête SQL.
        user: Identifiant de l'utilisateur.
        val: Valeurs utilisées dans la requête (optionnel).
    """

    if val is not None:
        logging.info(
            f"User ID {user}: Query executed successfully: '{query}' with value '{val}'"
        )
    else:
        logging.info(f"User ID {user}: Query executed successfully: '{query}'")


def log_ko_query(query, user, val=None, error=None):
    """
    Journalise l'échec de l'exécution d'une requête.

    Args:
        query (str): Requête SQL.
        user: Identifiant de l'utilisateur.
        val: Valeurs utilisées dans la requête (optionnel).
        error: Message d'erreur (optionnel).
    """
    if val is not None:
        logging.error(
            f"User ID {user}: Error executing query '{query}' with value '{val}'. \n CAUSE :{error}"
        )
    else:
        logging.error(
            f"User ID {user}: Error executing query '{query}'. \n CAUSE : {error}"
        )


def log_user_to_mysql(username, password, database, host=None):
    if host is None:
        host = get_host_default_from_config()
    try:
        server_connection = create_server_connection(
            host,
            username,
            password,
            database=database,
        )
        return server_connection
    except Error as err:
        if "Access denied" in str(err):
            logging.error(
                f"Access denied for {username}: Check your username and password."
            )
        elif "Unknown database" in str(err):
            logging.error("Unknown database: Make sure the database exists.")
        else:
            logging.error(f"Error connecting to MySQL: '{err}'")
        raise err


def get_connect(database=None):
    connector_attempts = 3
    current_connector_attempt = 0

    while current_connector_attempt < connector_attempts:
        try:
            username, password = get_user_login()
            server_connection = log_user_to_mysql(username, password, database)
            connector = Connector(server_connection, username, password)
            return connector
        except Error as e:
            current_connector_attempt += 1
            if current_connector_attempt == connector_attempts:
                logging.error(
                    "Failed to connect after three attempts. Exiting application."
                )
                sys.exit()
            else:
                logging.error(
                    f"Error connecting to database: '{e}'. Retrying ({current_connector_attempt}/{connector_attempts})"
                )


class Connector:
    def __init__(
        self,
        server_connection,
        username: str = None,
        password: str = None,
        set_user=True,
    ):
        """
        Initialise un objet Connector pour la connexion à la base de données.

        Args:
            username (str): Nom d'utilisateur.
            password (str): Mot de passe.
            set_user (bool): Indique s'il faut définir l'utilisateur actuel.
        """
        self.current_connection = server_connection
        if set_user:
            self.current_user = self.set_current_user(username, password)

        self.default_host = get_host_default_from_config()

    def reset_connection(self):
        print("Vous allez devoir vous reconnecter avant de poursuivre.")
        username, password = get_user_login()
        self.current_connection = log_user_to_mysql(username, password, "epicevent")

        self.current_user = self.set_current_user(username, password)

    def get_last_inserted_id(self):
        """
        Récupère l'ID du dernier élément inséré dans la base de données.

        Returns:
            int: ID du dernier élément inséré.
        """
        try:
            cursor = self.current_connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            logging.warning(f"Erreur lors de la récupération de l'ID : {e}")
        finally:
            if cursor:
                cursor.close()

    def set_current_user(self, username, password):
        """
        Définit l'utilisateur actuel en fonction du nom d'utilisateur et du mot de passe.

        Args:
            username (str): Nom d'utilisateur.
            password (str): Mot de passe haché et salé.
        """
        try:
            query = "SELECT * from collaborator where username = %s AND password = %s"
            val = (username, password)
            user_data = self.get_query_result(
                query,
                val,
                True,
            )
            collaborator = Collaborator(**dict(zip(*user_data)))
            return collaborator

        except Error as e:
            print(
                "Erreur lors de la récupération de l'utilisateur connecter. Veuillez contacter un administrateur"
            )
            logging.warning(f"Utilisateur inconnu sur le système CRM. : {e}")
            return None

    def get_current_user_id(self):
        """
        Récupère l'identifiant de l'utilisateur actuel.

        Returns:
            str: Identifiant de l'utilisateur.
        """
        return (
            getattr(self.current_user, "id", "unknown")
            if hasattr(self, "current_user")
            else "unknown"
        )

    def log_ok_query(self, query, val=None):
        user_id = self.get_current_user_id()
        log_ok_query(query, user_id, val)

    def log_ko_query(self, query, val=None, error=None):
        user_id = self.get_current_user_id()
        log_ko_query(query, user_id, val, error)

    def get_query_result(self, query, val, include_fields):
        try:
            result = get_query_result(
                query, val, include_fields, self.current_connection
            )
            self.log_ok_query(query)
            return result
        except Exception as query_error:
            self.log_ko_query(query, error=str(query_error))
            raise query_error

    def execute_query_w_val(self, query, val):
        """
        Exécute une requête SQL avec des valeurs.

        Args:
            query (str): Requête SQL.
            val: Valeurs à utiliser dans la requête.

        Returns:
            bool: True si l'exécution réussit, sinon False.

        Raises:
            Exception: Erreur lors de l'exécution de la requête.
        """
        try:
            result = execute_query_w_val(self.current_connection, query, val)
            self.log_ok_query(query, val)
            return result
        except Exception as query_error:
            self.log_ko_query(query, val, error=str(query_error))
            raise query_error

    def create(self, table, obj_dict):
        """
        Crée un enregistrement dans la table spécifiée.

        Args:
            table (str): Nom de la table.
            obj_dict (dict): Dictionnaire des valeurs à insérer dans la table.

        Returns:
            None
        """
        try:
            query = f"""INSERT INTO {table} {construct_col_name_for_query(obj_dict)} 
                                VALUES (%s{', %s' * (len(obj_dict) -1)})"""
            values = construct_val_name_for_query(obj_dict)

            self.execute_query_w_val(query, values)
            return
        except Error as e:
            if "INSERT command denied" in str(e):
                print("Vous n'avez pas les droits requis pour faire ceci.")

    def read(self, query, val=(), include_fields=True):
        results = self.get_query_result(
            query=query, val=val, include_fields=include_fields
        )
        return results

    def update(self, table_or_view, obj_dict, id):
        """
        Met à jour un enregistrement dans la table ou la vue spécifiée.

        Args:
            table_or_view (str): Nom de la table ou de la vue.
            obj_dict (dict): Dictionnaire des valeurs à mettre à jour.
            id: Identifiant de l'enregistrement à mettre à jour.

        Returns:
            None

        Raises:
            Error: Erreur lors de la mise à jour de l'enregistrement.
        """
        query = f"""UPDATE {table_or_view} SET {construct_col_name_for_update(obj_dict)} 
                                            WHERE {table_or_view}_id = %s
                                """
        val = construct_val_for_update(obj_dict)
        val.append(str(id))
        try:
            self.execute_query_w_val(query, val)
        except Error as e:
            if "UPDATE command denied" in str(e):
                self.log_ko_query(
                    query,
                    val,
                    error=f"\n Les droits ne semble pas permettre cette action à l'utilisateur : \n {e}",
                )
