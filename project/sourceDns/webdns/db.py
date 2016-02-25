import MySQLdb as mdb

def connMysql():
    host = '127.0.0.1'
    user = 'root'
    port = 3306
    db = 'webDns'
    conn = mdb.connect(host=host,
               port=port,
               user=user,
               db=db,
               charset='utf8',
               use_unicode=True)
    cur = conn.cursor()
    return cur

def mdelete():
    cur = connMysql()
    sql = "delete from webdns_upload" 
    cur.execute(sql)

def select():
    cur = connMysql()
    sql = "select * from webdns_upload"
    cur.execute(sql)
    query = cur.fetchone()[1]
    return query
