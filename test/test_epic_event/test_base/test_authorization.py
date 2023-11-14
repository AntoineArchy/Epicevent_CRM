from epic_event_CRM.base import roles
from epic_event_CRM.base.authorization import (
    BaseAuthorization,
    IsCollaborator,
    IsSupport,
    IsCommercial,
    IsGestion,
    IsNotSupport,
)
import pytest

from epic_event_CRM.collaborator.model import Collaborator


@pytest.fixture
def mock_user():
    return Collaborator()


def test_base_authorization(mock_user):
    authorization = BaseAuthorization()
    assert not authorization.has_authorization(mock_user)


def test_is_collaborator(mock_user):
    assert IsCollaborator.has_authorization(mock_user)


def test_is_commercial(mock_user):
    authorization = IsCommercial()
    assert not authorization.has_authorization(mock_user)
    mock_user.department = roles.EpicEventRole.commercial.value
    assert authorization.has_authorization(mock_user)


def test_is_support(mock_user):
    authorization = IsSupport()
    assert not authorization.has_authorization(mock_user)
    mock_user.department = roles.EpicEventRole.support.value
    assert authorization.has_authorization(mock_user)


def test_is_not_support(mock_user):
    authorization = IsNotSupport()
    assert authorization.has_authorization(mock_user)

    mock_user.department = roles.EpicEventRole.commercial.value
    assert authorization.has_authorization(mock_user)

    mock_user.department = roles.EpicEventRole.commercial.value
    assert authorization.has_authorization(mock_user)

    mock_user.department = roles.EpicEventRole.support.value
    assert not authorization.has_authorization(mock_user)


def test_is_gestion(mock_user):
    authorization = IsGestion()
    assert not authorization.has_authorization(mock_user)
    mock_user.department = roles.EpicEventRole.gestion.value
    assert authorization.has_authorization(mock_user)
