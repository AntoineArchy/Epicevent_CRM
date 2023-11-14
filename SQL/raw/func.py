GET_ID_FUNC = """
CREATE FUNCTION get_collaborator_id() RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE user_name VARCHAR(255);
  SET user_name = SUBSTRING_INDEX(USER(),'@',1);
  RETURN (SELECT collaborator_id FROM collaborator WHERE collaborator.username = user_name);
END;
"""

CREATE_QUERY_LIST = [GET_ID_FUNC]
