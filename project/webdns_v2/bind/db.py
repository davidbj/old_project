import MySQLdb as mdb

def connMysql():
    host = 'x.x.x.x'
    user = 'dns_bk_source_w'
    port = 3308
    db = 'mydns'
    
    conn = mdb.connect(host=host,
               port=port,
               user=user,
               db=db,
               charset='utf8',
               passwd='UeTp5FLOUk8y',
               use_unicode=True)
    cur = conn.cursor()
    return cur

def mdelete():
    cur = connMysql()
    sql = "delete from bind_upload" 
    cur.execute(sql)

def select():
    cur = connMysql()
    sql = "select * from bind_upload"
    cur.execute(sql)
    query = cur.fetchone()[1]
    return query
