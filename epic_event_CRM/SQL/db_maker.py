from mysql.connector import Error

from epic_event_CRM.SQL.raw.db_conf import RESET_CONF_QUERY_LIST, SET_CONF_QUERY_LIST
from epic_event_CRM.SQL.raw.func import (
    CREATE_FUNC_PROC_QUERY_LIST,
    DROP_FUNC_PROC_QUERY_LIST,
)
from epic_event_CRM.SQL.raw.make_db import CREATE_DB_QUERY, DROP_DB_QUERY
from epic_event_CRM.SQL.raw.privileges import (
    REVOKE_PRIVILEGE_QUERY_LIST,
    ADD_PRIVILEGE_QUERY_LIST,
)
from epic_event_CRM.SQL.raw.roles import CREATE_ROLE_QUERY_LIST, DROP_ROLE_QUERY_LIST
from epic_event_CRM.SQL.raw.tables import CREATE_TABLE_QUERY_LIST
from epic_event_CRM.SQL.raw.trigger import (
    CREATE_TRIGGER_QUERY_LIST,
    DROP_TRIGGER_QUERY_LIST,
)
from epic_event_CRM.SQL.raw.views import CREATE_VIEW_QUERY_LIST, DROP_VIEW_QUERY_LIST


def create_database(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_DB_QUERY)
        print("Base de données 'epicevent' créée avec succès.")
    except Error as e:
        print(f"Erreur lors de la création de la base de données : {e}")
        raise e


def drop_database(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(DROP_DB_QUERY)
        print("Base de données 'epicevent' supprimée avec succès.")
    except Error as e:
        print(f"Erreur lors de la suppression de la base de données : {e}")
        raise e


def use_epic(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("USE epicevent;")
            cursor.close()
            print("Base de données 'epicevent' sélectionnée.")
    except Error as e:
        print(f"Erreur lors de la sélection de la base de données 'epicevent' : {e}")


def set_database_config(connection):
    try:
        with connection.cursor() as cursor:
            for query in SET_CONF_QUERY_LIST:
                cursor.execute(query)
        print("Configuration de la base de données mise à jour avec succès.")
    except Error as e:
        print(
            f"Erreur lors de la mise à jour de la configuration de la base de données : {e}"
        )
        raise e


def drop_database_config(connection):
    try:
        with connection.cursor() as cursor:
            for query in RESET_CONF_QUERY_LIST:
                cursor.execute(query)
        print("Configuration de la base de données supprimée avec succès.")
    except Error as e:
        print(
            f"Erreur lors de la suppression de la configuration de la base de données : {e}"
        )
        raise e


def create_functions_procedures(connection):
    try:
        with connection.cursor() as cursor:
            for query in CREATE_FUNC_PROC_QUERY_LIST:
                cursor.execute(query)
            print("Fonctions et procédures créées avec succès.")
    except Error as e:
        print(f"Erreur lors de la création des fonctions et procédures : {e}")
        raise e


def drop_functions_procedures(connection):
    try:
        with connection.cursor() as cursor:
            for query in DROP_FUNC_PROC_QUERY_LIST:
                cursor.execute(query)
            print("Fonctions et procédures supprimées avec succès.")
    except Error as e:
        print(f"Erreur lors de la suppression des fonctions et procédures : {e}")
        raise e


def revoke_privileges(connection):
    try:
        with connection.cursor() as cursor:
            for privilege in REVOKE_PRIVILEGE_QUERY_LIST:
                cursor.execute(privilege)
            connection.commit()
            print("Privilèges révoqués avec succès.")
    except Error as e:
        print(f"Erreur lors de la révocation des privilèges : {e}")
        raise e


def add_privileges(connection):
    try:
        with connection.cursor() as cursor:
            for query in ADD_PRIVILEGE_QUERY_LIST:
                cursor.execute(query)
            print("Privilèges ajoutés avec succès.")
    except Error as e:
        print(f"Erreur lors de l'ajout des privilèges : {e}")
        raise e


def role_exists(cursor, role_name):
    cursor.execute(f"SELECT 1 FROM mysql.user WHERE user = '{role_name}'")
    return cursor.fetchone() is not None


def create_roles(connection):
    try:
        with connection.cursor() as cursor:
            for query in CREATE_ROLE_QUERY_LIST:
                role_name = query.split()[-1].strip(
                    "'"
                )  # Récupérer le nom du rôle à partir de la requête
                if not role_exists(cursor, role_name):
                    cursor.execute(query)
                    print(f"Rôle {role_name} créé avec succès.")
                else:
                    print(f"Le rôle {role_name} existe déjà.")
    except Error as e:
        print(f"Erreur lors de la création des rôles : {e}")
        raise e


def drop_roles(connection):
    try:
        with connection.cursor() as cursor:
            for query in DROP_ROLE_QUERY_LIST:
                role_name = query.split()[-1].strip(
                    "'"
                )  # Récupérer le nom du rôle à partir de la requête
                if role_exists(cursor, role_name):
                    cursor.execute(query)
                    print(f"Rôle {role_name} supprimé avec succès.")
                else:
                    print(f"Le rôle {role_name} n'existe pas.")
    except Error as e:
        print(f"Erreur lors de la suppression des rôles : {e}")
        raise e


def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None


def create_tables(connection):
    try:
        with connection.cursor() as cursor:
            for query in CREATE_TABLE_QUERY_LIST:
                query_type = query.split()[0].upper()  # Récupère le type de requête
                if query_type == "CREATE":
                    table_name = query.split()[
                        2
                    ]  # Récupère le nom de la table à partir de la requête
                    if not table_exists(cursor, table_name):
                        cursor.execute(query)
                        print(f"Table {table_name} créée avec succès.")
                    else:
                        print(f"La table {table_name} existe déjà.")
                elif query_type == "ALTER":
                    cursor.execute(query)
                    print("Opération ALTER exécutée avec succès.")
    except Error as e:
        print(f"Erreur lors de la création des tables : {e}")
        raise e


def drop_tables(connection):
    try:
        with connection.cursor() as cursor:
            # Dans l'ordre inverse de la création pour respecter les contraintes de clé étrangère
            for query in reversed(CREATE_TABLE_QUERY_LIST):
                table_name = query.split()[2]  # Récupère le nom de la table
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print("Tables supprimées avec succès.")
    except Error as e:
        print(f"Erreur lors de la suppression des tables : {e}")
        raise e


def create_triggers(connection):
    try:
        with connection.cursor() as cursor:
            for query in CREATE_TRIGGER_QUERY_LIST:
                cursor.execute(query)
            print("Déclencheurs créés avec succès.")
    except Error as e:
        print(f"Erreur lors de la création des déclencheurs : {e}")
        raise e


def drop_triggers(connection):
    try:
        with connection.cursor() as cursor:
            for query in DROP_TRIGGER_QUERY_LIST:
                cursor.execute(query)
            print("Déclencheurs supprimés avec succès.")
    except Error as e:
        print(f"Erreur lors de la suppression des déclencheurs : {e}")
        raise e


def create_views(connection):
    try:
        with connection.cursor() as cursor:
            for query in CREATE_VIEW_QUERY_LIST:
                cursor.execute(query)
            print("Vues créées avec succès.")
    except Error as e:
        print(f"Erreur lors de la création des vues : {e}")
        raise e


def drop_views(connection):
    try:
        with connection.cursor() as cursor:
            for query in DROP_VIEW_QUERY_LIST:
                cursor.execute(query)
            print("Vues supprimées avec succès.")
    except Error as e:
        print(f"Erreur lors de la suppression des vues : {e}")
        raise e
