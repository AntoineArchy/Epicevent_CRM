from sqlite3 import Connection

from SQL.raw import make_db, tables, roles, privileges, func, views, trigger, db_conf


def create_db(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.CREATE_DB_QUERY)

    except:
        pass


def drop_db(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.DROP_DB_QUERY)

    except:
        pass


def create_tables(cursor: Connection.cursor):
    try:
        cursor.executemany(tables.CREATE_QUERY_LIST)

    except:
        pass


def drop_table(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def create_roles(cursor: Connection.cursor):
    try:
        cursor.executemany(roles.CREATE_QUERY_LIST)

    except:
        pass


def drop_roles(cursor: Connection.cursor):
    try:
        cursor.executemany(roles.DROP_QUERY_LIST)

    except:
        pass


def create_privileges(cursor: Connection.cursor):
    try:
        cursor.executemany(privileges.CREATE_QUERY_LIST)

    except:
        pass


def drop_privileges(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def create_func(cursor: Connection.cursor):
    try:
        cursor.executemany(func.CREATE_QUERY_LIST)

    except:
        pass


def drop_func(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def create_views(cursor: Connection.cursor):
    try:
        cursor.executemany(views.CREATE_QUERY_LIST)

    except:
        pass


def drop_views(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def create_trigger(cursor: Connection.cursor):
    try:
        cursor.executemany(trigger.CREATE_QUERY_LIST)

    except:
        pass


def drop_trigger(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.CREATE_DB_QUERY)

    except:
        pass


def create_db_conf(cursor: Connection.cursor):
    try:
        cursor.executemany(db_conf.CREATE_QUERY_LIST)

    except:
        pass


def drop_db_conf(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def do_db_dump(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def load_db_dump(cursor: Connection.cursor):
    try:
        cursor.execute(make_db.D)

    except:
        pass


def init_base(cursor: Connection.cursor):
    create_db(cursor)
    create_tables(cursor)
    create_roles(cursor)
    create_privileges(cursor)
    create_func(cursor)
    create_views(cursor)
    create_trigger(cursor)
    create_db_conf(cursor)


def erase_user(cursor: Connection.cursor):
    pass


def erase_base(cursor: Connection.cursor, erase_mysql_user=False):
    drop_db_conf(cursor)
    drop_trigger(cursor)
    drop_views(cursor)
    drop_func(cursor)
    drop_privileges(cursor)
    drop_roles(cursor)
    drop_table(cursor)
    drop_db(cursor)

    if erase_mysql_user:
        erase_user(cursor)


def reset_base(cursor: Connection.cursor, erase_mysql_user=False):
    do_db_dump(cursor)
    erase_base(cursor)
    init_base(cursor)
