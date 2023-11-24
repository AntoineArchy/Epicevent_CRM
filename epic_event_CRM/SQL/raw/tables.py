CREATE_COLLABORATEURS_QUERY = """
CREATE TABLE collaborator (
  collaborator_id INT AUTO_INCREMENT PRIMARY KEY,
  department VARCHAR(20),
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  username VARCHAR(30) NOT NULL,
  password VARCHAR(60) NOT NULL,
  creation_date DATE NOT NULL,
  last_update DATETIME,
  is_active BOOLEAN DEFAULT TRUE
  );
 """
CREATE_CLIENT_QUERY = """
CREATE TABLE client (
  client_id INT AUTO_INCREMENT PRIMARY KEY,
  collaborator_id INT,
  full_name VARCHAR(40) NOT NULL,
  company_name VARCHAR(40) NOT NULL,
  email VARCHAR(30) NOT NULL,
  phone VARCHAR(30) NOT NULL,
  creation_date DATE NOT NULL,
  last_update DATETIME,
  is_active BOOLEAN DEFAULT TRUE
  );
 """

CREATE_CONTRACT_QUERY = """
CREATE TABLE contract (
  contract_id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT,
  cost FLOAT,
  balance FLOAT,
  statut VARCHAR(20),
  creation_date DATE,
  last_update DATETIME,
  is_active BOOLEAN DEFAULT TRUE
  );
 """

CREATE_EVENT_QUERY = """
CREATE TABLE event (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  contract_id INT,
  support_contact INT DEFAULT NULL,
  name VARCHAR(30),
  event_start DATETIME,
  event_end DATETIME,
  location VARCHAR(50),
  attendees INT,
  notes TINYTEXT,
  creation_date DATE,
  last_update DATETIME,
  is_active BOOLEAN DEFAULT TRUE
);
"""

ALTER_CLIENT = """
ALTER TABLE client
ADD FOREIGN KEY(collaborator_id)
REFERENCES collaborator(collaborator_id)
ON DELETE SET NULL;
"""

ALTER_CONTRACT = """
ALTER TABLE contract
ADD FOREIGN KEY(client_id)
REFERENCES client(client_id)
ON DELETE SET NULL;
"""

ALTER_EVENT_1 = """
ALTER TABLE event
ADD FOREIGN KEY(contract_id)
REFERENCES contract(contract_id)
ON DELETE SET NULL;
"""

ALTER_EVENT_2 = """
ALTER TABLE event
ADD FOREIGN KEY(support_contact)
REFERENCES collaborator(collaborator_id)
ON DELETE SET NULL;
"""

CREATE_TABLE_QUERY_LIST = [
    CREATE_COLLABORATEURS_QUERY,
    CREATE_CLIENT_QUERY,
    CREATE_CONTRACT_QUERY,
    CREATE_EVENT_QUERY,
    ALTER_CLIENT,
    ALTER_CONTRACT,
    ALTER_EVENT_1,
    ALTER_EVENT_2,
]
