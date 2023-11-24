from base.roles import EpicEventRole


class BaseAuthorization:
    """
    Classe de base pour les autorisations.

    Les classes dérivées doivent implémenter la méthode `has_authorization`.
    """

    @staticmethod
    def has_authorization(user):
        """
        Vérifie si l'utilisateur a l'autorisation.

        Args:
            user (User): L'objet utilisateur.

        Returns:
            bool: True si l'utilisateur a l'autorisation, False sinon.
        """
        return False


class IsCollaborator(BaseAuthorization):
    @staticmethod
    def has_authorization(user):
        return user.has_role(EpicEventRole.collaborator)


class IsCommercial(BaseAuthorization):
    @staticmethod
    def has_authorization(user):
        return user.has_role(EpicEventRole.commercial)


class IsSupport(BaseAuthorization):
    @staticmethod
    def has_authorization(user):
        return user.has_role(EpicEventRole.support)


class IsNotSupport(BaseAuthorization):
    @staticmethod
    def has_authorization(user):
        return not user.has_role(EpicEventRole.support)


class IsGestion(BaseAuthorization):
    @staticmethod
    def has_authorization(user):
        return user.has_role(EpicEventRole.gestion)


class Forbidden(BaseAuthorization):
    @staticmethod
    def has_authorization(user):
        return False
