SET_COLLABORATOR_ROLE_AS_MANDATORY = "SET PERSIST mandatory_roles = 'collaborator';"
DB_CONF_SET_AUTO_ROLE_ON_LOGIN = "SET PERSIST activate_all_roles_on_login = ON;"

RESET_DEFAULT_ROLE = "SET PERSIST mandatory_roles = DEFAULT"
RESET_DEFAULT_ROLE_ON_LOGIN = "SET PERSIST activate_all_roles_on_login = DEFAULT"

RESET_CONF_QUERY_LIST = [RESET_DEFAULT_ROLE, RESET_DEFAULT_ROLE_ON_LOGIN]
SET_CONF_QUERY_LIST = [SET_COLLABORATOR_ROLE_AS_MANDATORY, DB_CONF_SET_AUTO_ROLE_ON_LOGIN]
