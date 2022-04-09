import pymysql
from config.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


class MySQLDB:

    def __init__(self, host, port, user, password, dbname):
        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=dbname,
            autocommit=True
        )
        # 创建游标 并且使用字典型返回对象
        self.cur = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.cur.close()
        self.db.close()

    """查询"""

    def select_db(self, sql):
        # 如果断开则重新连接
        self.db.ping(reconnect=True)
        # 执行
        self.cur.execute(sql)
        # 返回结果
        data = self.cur.fetchall()
        return data

    """增 删 改"""

    def execute_db(self, sql):
        try:
            self.db.ping(reconnect=True)
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print("操作出现错误：%s" % e)
            self.db.rollback()


db = MySQLDB(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
