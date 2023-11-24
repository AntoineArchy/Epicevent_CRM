from .db_maker import (
    create_database,
    use_epic,
    create_tables,
    create_roles,
    create_functions_procedures,
    add_privileges,
    create_views,
    create_triggers,
    set_database_config,
    drop_database_config,
    drop_triggers,
    drop_views,
    drop_functions_procedures,
    revoke_privileges,
    drop_roles,
    drop_tables,
    drop_database,
)

# Liste des opérations de création de la base de données
CREATE_DATABASE_OPERATIONS = [
    create_database,
    use_epic,
    create_tables,
    create_roles,
    create_functions_procedures,
    add_privileges,
    create_views,
    create_triggers,
    set_database_config,
]

# Liste des opérations de destruction de la base de données
DROP_DATABASE_OPERATIONS = [
    drop_database_config,
    drop_triggers,
    drop_views,
    drop_functions_procedures,
    revoke_privileges,
    drop_roles,
    drop_tables,
    drop_database,
]
