import configparser

import bcrypt


def is_valid_password(password):
    """
    Vérifie si le mot de passe respecte les critères du RGPD.
    """
    # Au moins 8 caractères
    if len(password) < 8:
        return False

    # Au moins une lettre majuscule
    if not any(char.isupper() for char in password):
        return False

    # Au moins une lettre minuscule
    if not any(char.islower() for char in password):
        return False

    # Au moins un chiffre
    if not any(char.isdigit() for char in password):
        return False

    # Au moins un caractère spécial
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
    if not any(char in special_characters for char in password):
        return False

    # Pas d'espaces
    if " " in password:
        return False

    return True


def get_host_default_from_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "database" in config and "host_default" in config["database"]:
        return config["database"]["host_default"]
    else:
        host_default = input(
            "Veuillez fournir le host par défaut (appuyez sur Entrée pour utiliser 'localhost') : "
        ).strip()
        return host_default if host_default else "localhost"


def get_sentry_link_from_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "logging" in config and "sentry_url" in config["logging"]:
        return config["logging"]["sentry_url"]
    else:
        return False


def get_salt_from_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "security" in config and "salt" in config["security"]:
        return config["security"]["salt"]
    else:
        raise ValueError("Salt not found in the configuration file.")


def hash_password(password):
    salt = get_salt_from_config()

    # Hacher le mot de passe avec le sel
    hashed_password_bytes = bcrypt.hashpw(
        password.encode("utf-8"), salt.encode("utf-8")
    )
    hashed_password_str = hashed_password_bytes.decode("utf-8")

    return hashed_password_str
