import pymysql
import pandas as pd


class TestDB:
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', port=3306,
                                  user='root', passwd='@science9110',
                                  db='test', charset='utf8')


    def select_all(self):
        cursor = self.db.cursor()
        sql = 'select * from test.table1'
        cursor.execute(sql)

        cursor.execute("CREATE TABLE customers(name VARCHAR(255), address VARCHAR(255))")
        cursor.execute("SHOW TABLES")
        for x in cursor:
            print(x)

        result = cursor.fetchone()
        result = pd.DataFrame(result)
        return result


