import sqlite3

__connection = sqlite3.connect("db_sqlite\db_music.sqlite", check_same_thread=False)
__cursor = __connection.cursor()


def select_c1_from_t1(c1, t1):
    return __cursor.execute("SELECT {0} FROM {1}".format(c1, t1)).fetchall()


def select_c1_from_t1_where_c2_eq_v2(c1, t1, c2, v2):
    query = "SELECT {0} FROM {1} WHERE {2} = '{3}'".format(c1, t1, c2, v2)
    return __cursor.execute(query).fetchall()


def select_cn_from_t1(t1, cn):
    cn = ', '.join(cn)
    return __cursor.execute("SELECT {0} FROM {1}".format(cn, t1)).fetchall()


def select_cn_from_t1_where_c1_eq_v1(cn, t1, c1, v1):
    cn = ', '.join(cn)
    return __cursor.execute("SELECT {0} FROM {1} WHERE {2} = '{3}'".format(cn, t1, c1, v1)).fetchall()


def select_cn_from_tn_where_complex_condition(cn, tn, cc):
    cn = ', '.join(cn)
    tn = ', '.join(tn)
    query = "SELECT {0} FROM {1} WHERE {2}".format(cn, tn, cc)
    return __cursor.execute(query).fetchall()


def update_t1_set_c1_eq_v1(t1, c1, v1):
    __cursor.execute("UPDATE {0} SET {1} = '{2}'".format(t1, c1, v1))
    __connection.commit()


def update_t1_set_c1_eq_v1_where_c2_eq_v2(t1, c1, v1, c2, v2):
    __cursor.execute("UPDATE {0} SET {1} = '{2}' WHERE {3} = '{4}'".format(t1, c1, v1, c2, v2))
    __connection.commit()


def update_t1_set_cvn_where_c2_eq_v2(t1, cvn, c2, v2):
    __cursor.execute("UPDATE {0} SET {1} WHERE {2} = '{3}'".format(t1, cvn, c2, v2))
    __connection.commit()


def insert_into_t1_pn_values_vn(t1, pn, vn):
    vn = ', '.join("'{0}'".format(t) for t in vn)
    pn = ', '.join(pn)
    __cursor.execute("INSERT INTO {0} ({1}) VALUES ({2})".format(t1, pn, vn))
    __connection.commit()


def delete_from_t1_where_c1_eq_v1(t1, c1, v1):
    __cursor.execute("DELETE FROM {0} WHERE {1} = '{2}'".format(t1, c1, v1))
    __connection.commit()
