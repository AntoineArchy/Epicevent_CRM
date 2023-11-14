from epic_event_CRM.base.roles import EpicEventRole


class BaseAuthorization:
    @staticmethod
    def has_authorization(user):
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
