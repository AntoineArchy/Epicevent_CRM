CREATE_GET_ID_FUNC = """
CREATE FUNCTION get_collaborator_id() RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE user_name VARCHAR(255);
  SET user_name = SUBSTRING_INDEX(USER(),'@',1);
  RETURN (SELECT collaborator_id FROM collaborator WHERE collaborator.username = user_name);
END;
"""

CREATE_SET_ROLE_PROC = """
CREATE PROCEDURE AssignRoleToCollaborator (IN collaboratorName VARCHAR(255), IN roleName VARCHAR(255))
BEGIN
    SET @roleQuery = CONCAT('GRANT ', roleName, ' TO ', collaboratorName); 

    PREPARE stmt FROM @roleQuery;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END;
"""

DROP_GET_ID_FUNC = "DROP FUNCTION IF EXISTS get_collaborator_id"
DROP_SET_ROLE_PROC = "DROP PROCEDURE IF EXISTS AssignRoleToCollaborator",

CREATE_FUNC_PROC_QUERY_LIST = [CREATE_GET_ID_FUNC, CREATE_SET_ROLE_PROC]
DROP_FUNC_PROC_QUERY_LIST = [DROP_GET_ID_FUNC, DROP_SET_ROLE_PROC]




