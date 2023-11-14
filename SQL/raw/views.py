COLLABORATEUR_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_collaborator AS 
SELECT 
  department AS 'Département', 
  first_name AS 'Nom', 
  last_name AS 'Prénom', 
  username AS 'Nom affiché', 
  creation_date AS 'Collaborateur depuis' 
FROM collaborator;
"""

CLIENT_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_client AS 
SELECT 
  client_id AS 'Client ID',
  company_name AS 'Société', 
  full_name AS 'Intérlocuteur', 
  email AS 'adresse mail', 
  phone AS 'téléphone', 
  creation_date AS 'client depuis', 
  last_update AS 'dernier contact', 
  collaborator_id AS 'Commercial associé' 
FROM client;
"""


CONTRACT_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_contract AS 
SELECT 
  contract_id AS `Contrat ID`,
  client_id AS 'Client ID', 
  cost AS 'Cout', 
  balance AS 'Balance', 
  statut AS 'Statut', 
  creation_date AS 'Sous contrat depuis' 
FROM contract;
"""


EVENT_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_event AS 
SELECT 
  contract_id AS `Contrat ID`,
  event_id AS 'Event ID',
  name AS 'Événement', 
  event_start AS 'Début', 
  event_end AS 'Fin', 
  location AS 'Lieu', 
  attendees AS 'Participants', 
  notes AS 'Notes' 
FROM event;
"""

COMMERCIAL_OWN_CLIENT_VIEW = """
CREATE OR REPLACE VIEW epicevent.commercial_own_client AS
SELECT * FROM epicevent.list_client
WHERE `Commercial associé` = get_collaborator_id();
"""

COMMERCIAL_CLIENT_CONTRACT_VIEW = """
CREATE OR REPLACE VIEW epicevent.commercial_client_contracts AS
SELECT * FROM list_contract 
WHERE `Client ID` IN (
SELECT DISTINCT(client_id) FROM client
WHERE collaborator_id = get_collaborator_id());
"""

COMMERCIAL_CLIENT_EVENT_VIEW = """
CREATE OR REPLACE VIEW epicevent.commercial_client_event_view AS
SELECT * FROM list_event
WHERE `Contrat ID` IN (
  SELECT `Contrat ID` 
  FROM commercial_own_client );

"""

GESTION_UNASSIGNED_EVENT = """
CREATE OR REPLACE VIEW epicevent.unassigned_event AS
SELECT * FROM event
WHERE support_contact IS NULL;
"""

SUPPORT_ASSIGNEE_EVENT = """
CREATE OR REPLACE VIEW epicevent.user_assigned_event AS
SELECT * FROM event
WHERE support_contact = get_collaborator_id();
"""

CREATE_QUERY_LIST = [
    COLLABORATEUR_FULL_VIEW,
    CLIENT_FULL_VIEW,
    CONTRACT_FULL_VIEW,
    EVENT_FULL_VIEW,
    COMMERCIAL_OWN_CLIENT_VIEW,
    COMMERCIAL_CLIENT_CONTRACT_VIEW,
    GESTION_UNASSIGNED_EVENT,
    SUPPORT_ASSIGNEE_EVENT,
]
