AUTO_ASSIGN_COMMERCIAL_TO_CLIENT = """
CREATE TRIGGER auto_assign_commercial_to_client BEFORE INSERT ON client
FOR EACH ROW 
SET new.collaborator_id = get_collaborator_id();
"""

CREATE_QUERY_LIST = [AUTO_ASSIGN_COMMERCIAL_TO_CLIENT]
