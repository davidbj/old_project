import pymysql
from mqORM.utils import DB_HOST, DB_PORT, DB_PASSWD, DB_USER, DEFAULT_DB, DEFAULT_CHARSET


class DB(object):

    def __init__(self, **kwargs):
        if 'charset' not in kwargs:
            kwargs['charset'] = 'utf8'

        if 'autocommit' not in kwargs:
            kwargs['autocommit'] = True

        try:
            self.conn = pymysql.connect(**kwargs)
            self.cur = self.conn.cursor()
        except:
            print("Connection time out!")

    def execute(self, sql, args=None):
        return self.cur.execute(sql, args)

    def select(self, sql, args=None):
        self.execute(sql, args)
        return self.get_rows()

    def insert(self, table, column_dict):
        ld_key = []
        values = []
        for k, v in column_dict.items():
            ld_key.append(k)
            values.append(v)

        keys = '`,`'.join(ld_key)
        placeholder = ','.join(['\'%s\'' for v in values])
        sql = 'INSERT INTO %(table)s (`%(keys)s`) VALUES (%(placeholder)s)' % locals(
        )
        return self.execute(sql % tuple(['%s' % i for i in values]))

    def get_rows(self, size=None, is_dict=False):
        if size is None:
            rows = self.cur.fetchall()

        if rows is None:
            rows = []
        return rows

    def __del__(self):
        self.close()

    def close(self):
        self.cur.close()
        self.conn.close()


def connDb():
    return DB(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        passwd=DB_PASSWD,
        db=DEFAULT_DB)

# if __name__ == "__main__":
#    conn = DB(host='localhost', port=3306, user='root', passwd='', db='mqorm')
#    conn.insert('db', {'name':'david', 'email':"test@test.com", 'password':'12'})
