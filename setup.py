import configparser
import os
import sys

import bcrypt
from mysql.connector import Error

from base.connector import get_user_login, log_user_to_mysql, Connector
from base.roles import EpicEventRole
from epic_event_CRM.SQL import CREATE_DATABASE_OPERATIONS, DROP_DATABASE_OPERATIONS
from epic_event_CRM.collaborator.controller import CollaboratorController
from epic_event_CRM.collaborator.model import Collaborator


def validate_salt(salt):
    try:
        bcrypt.hashpw(b"password", salt.encode("utf-8"))
        return True
    except ValueError:
        return False


def get_confirmation(message="Êtes vous sur ?", yes="o", no="n"):
    user_choice = input(f"{message} {yes}/{no} : ").lower().strip()
    if user_choice not in [yes.lower(), no.lower()]:
        print(f"Veuillez répondre par {yes} où {no}")
        return get_confirmation(message, yes, no)
    return user_choice == yes.lower()


def ask_host():
    host_default = input(
        "Veuillez fournir le host par défaut (appuyez sur Entrée pour utiliser 'localhost') : "
    ).strip()
    return host_default if host_default else "localhost"


def ask_salt():
    while True:
        # Demander à l'utilisateur s'il possède déjà un "salt"
        if get_confirmation(
            "Possédez-vous déjà un 'salt' pour l'encryptage des mots de passe ? \n "
            "Si 'Non', il sera généré automatiquement "
        ):
            salt = input("Veuillez entrer votre 'salt' : ")
            if validate_salt(salt):
                break
            else:
                print(
                    "Le 'salt' que vous avez fourni n'est pas valide. Veuillez réessayer."
                )
        else:
            # Générer automatiquement un "salt" avec bcrypt
            salt = bcrypt.gensalt().decode("utf-8")
            break
    return salt


def ask_sentry():
    if not get_confirmation("Avez vous un liens sentry ?"):
        print(
            "Vous pourrez l'ajoutez plus tard manuellement dans le fichier config.ini."
        )
        return False
    return True


def create_ini_file():
    config = configparser.ConfigParser()

    config["database"] = {}
    config["security"] = {}
    config["logging"] = {}

    config["database"]["host_default"] = ask_host()
    config["security"]["salt"] = ask_salt()
    if ask_sentry():
        config["logging"]["sentry_url"] = input("Entrez votre lien Sentry.")

    with open("config.ini", "w") as configfile:
        config.write(configfile)


def dump_base(connection):
    dump_filename = input("Nom du fichier de dump (ex: dump_epicevent.sql): ")
    with open(dump_filename, "w") as dump_file:
        dump_command = (
            f"mysqldump -u {connection.user} -p --databases epicevent > {dump_filename}"
        )
        os.system(dump_command)
        print(f"Dump de la base de données réalisé avec succès dans {dump_filename}")


def create_db_rules(connection):
    try:
        connection.start_transaction()

        for operation in CREATE_DATABASE_OPERATIONS:
            try:
                operation(connection)
            except Error as e:
                print(f"Erreur lors de l'exécution de l'opération : {e}")
                if not get_confirmation("Voulez-vous continuer malgré l'erreur ?"):
                    raise e  # Lève l'exception si l'utilisateur ne veut pas continuer
        connection.commit()
        return True

    except Error as e:
        # En cas d'erreur, annule la transaction
        print(f"Erreur lors de la configuration d'Epic Event : {e}")
        connection.rollback()
        raise e


def create_initial_collaborator(server_connection):
    print("Vous allez maintenant faire la création du premier utilisateur gestion.")
    connector = Connector(server_connection=server_connection, set_user=False)

    print("Création du premier collaborateur gestion:")
    first_name = input("Prénom: ")
    last_name = input("Nom: ")
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")

    # Création du collaborateur avec le département 'gestion'
    collaborator = Collaborator(
        department=EpicEventRole.gestion.value,
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
    )
    CollaboratorController.save(collaborator, connector, check_connection=False)


def setup_epic_event():
    print(
        "Nous allons dans un premier temps mettre en place le fichier de configuration."
    )
    create_ini_file()
    print(
        "Vous allez maintenant devoir vous connecter avec des identifiants "
        "ayants les droits administrateur sur le serveur MySql de l'hôte."
    )
    username, password = get_user_login(skip_hash=True)
    server_connection = log_user_to_mysql(
        username=username, password=password, database=None
    )

    create_db_rules(connection=server_connection)

    while True:
        try:
            create_initial_collaborator(server_connection=server_connection)
            break  # Sortir de la boucle si tout se passe bien
        except Error as e:
            print("Erreur lors de la création du premier collaborateur :")
            if "Operation CREATE USER failed" in str(e):
                print(
                    "Cette erreur est souvent due à un nom d'utilisateur déjà existant."
                )
            else:
                print("Veuillez vérifier les informations fournies.")
    return True


def uninstall_epic_event_confirm():
    username, password = get_user_login(skip_hash=True)
    server_connection = log_user_to_mysql(
        username=username, password=password, database="epicevent"
    )
    if get_confirmation(
        "Voulez-vous faire un dump de la base avant la désinstallation?"
    ):
        dump_base(connection=server_connection)
    try:
        server_connection.start_transaction()

        for operation in DROP_DATABASE_OPERATIONS:
            try:
                operation(server_connection)
            except Error as e:
                print(f"Erreur lors de l'exécution de l'opération : {e}")
                if not get_confirmation("Voulez-vous continuer malgré l'erreur ?"):
                    raise e  # Lève l'exception si l'utilisateur ne veut pas continuer
        server_connection.commit()
        return True

    except Error as e:
        # En cas d'erreur, annule la transaction
        print(f"Erreur lors de la désinstallation d'Epic Event : {e}")
        server_connection.rollback()
        raise e


def setup():
    print("Bienvenue dans la configuration d'Epic Event!")
    print(
        "Assurez-vous d'avoir un compte avec des droits d'administration sur le serveur mysql pour poursuivre."
    )
    action = input(
        "Voulez-vous mettre en place ou désinstaller Epic Event? (setup/uninstall): "
    ).lower()

    if action == "setup":
        try:
            setup_epic_event()
        except Exception as e:
            print(f"Sortie de l'installation de Epic Event CRM suite à l'erreur : {e}'")
            # Ajoutez ici tout code de nettoyage ou de gestion d'erreur supplémentaire si nécessaire
            sys.exit(1)  # Arrête le programme avec un code d'erreur
        print("Configuration d'Epic Event terminée avec succès.")
        print(
            "Vous pouvez à présent vous connecter à l'application avec les "
            "identifiants du premier utilisateur gestion."
        )
    elif action == "uninstall":
        try:
            if not get_confirmation(
                "Êtes-vous sûr de vouloir désinstaller Epic Event?"
            ):
                return

            uninstall_epic_event_confirm()

        except Exception as e:
            print(
                f"Sortie de la désinstallation de Epic Event CRM suite à l'erreur : {e}'"
            )
            # Ajoutez ici tout code de nettoyage ou de gestion d'erreur supplémentaire si nécessaire
            sys.exit(1)  # Arrête le programme avec un code d'erreur


setup()
