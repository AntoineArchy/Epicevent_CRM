COLLABORATEUR_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_collaborator AS 
SELECT 
  department AS 'Département', 
  first_name AS 'Prénom', 
  last_name AS 'Nom', 
  username AS 'Nom affiché', 
  creation_date AS 'Collaborateur depuis',
  collaborator_id AS 'Collaborateur ID',
  last_update AS 'Dernière MàJ',
  is_active AS 'Actif'
FROM collaborator
ORDER BY is_active DESC;
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
  last_update AS 'Dernière MàJ',
  collaborator_id AS 'Commercial associé' 
FROM client;
"""


CONTRACT_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_contract AS 
SELECT 
  c.contract_id AS `Contrat ID`,
  cl.client_id AS 'Client ID',
  CONCAT(cl.full_name, ' - ', cl.company_name) AS 'Client',
  c.cost AS 'Cout',
  c.balance AS 'Balance',
  c.statut AS 'Statut',
  c.creation_date AS 'Sous contrat depuis',
  c.last_update AS 'Dernière MàJ',
  c.is_active AS 'Actif'
FROM contract c
JOIN client cl ON c.client_id = cl.client_id;
"""


EVENT_FULL_VIEW = """
CREATE OR REPLACE VIEW epicevent.list_event AS 
SELECT 
  c.contract_id AS `Contrat ID`,
  e.event_id AS 'Event ID',
  e.support_contact AS 'Contact de support',
  e.name AS 'Événement', 
  e.event_start AS 'Début', 
  e.event_end AS 'Fin', 
  e.location AS 'Lieu', 
  e.attendees AS 'Participants', 
  e.notes AS 'Notes' ,
  e.last_update AS 'Dernière MàJ',
  CONCAT(cl.full_name, ' - ', cl.phone, ', ', cl.email) AS 'Contacts',
  cl.company_name AS 'Société'
FROM event e
JOIN contract c ON e.contract_id = c.contract_id
JOIN client cl ON c.client_id = cl.client_id;
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
SELECT * FROM list_event
WHERE `Contact de support` IS NULL;
"""

SUPPORT_ASSIGNEE_EVENT = """
CREATE OR REPLACE VIEW epicevent.user_assigned_event AS
SELECT * FROM list_event
WHERE `Contact de support` = get_collaborator_id();
"""

CREATE_VIEW_QUERY_LIST = [
    COLLABORATEUR_FULL_VIEW,
    CLIENT_FULL_VIEW,
    CONTRACT_FULL_VIEW,
    EVENT_FULL_VIEW,
    COMMERCIAL_OWN_CLIENT_VIEW,
    COMMERCIAL_CLIENT_CONTRACT_VIEW,
    COMMERCIAL_CLIENT_EVENT_VIEW,
    GESTION_UNASSIGNED_EVENT,
    SUPPORT_ASSIGNEE_EVENT,
]


DROP_VIEW_QUERY_LIST = [
    "DROP VIEW IF EXISTS epicevent.list_collaborator",
    "DROP VIEW IF EXISTS epicevent.list_client",
    "DROP VIEW IF EXISTS epicevent.list_contract",
    "DROP VIEW IF EXISTS epicevent.list_event",
    "DROP VIEW IF EXISTS epicevent.commercial_own_client",
    "DROP VIEW IF EXISTS epicevent.commercial_client_contracts",
    "DROP VIEW IF EXISTS epicevent.commercial_client_event_view",
    "DROP VIEW IF EXISTS epicevent.unassigned_event",
    "DROP VIEW IF EXISTS epicevent.user_assigned_event",
]
