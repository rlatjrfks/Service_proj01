import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook


# create table test(num int(11), name varchar(10))

class Test:
    def __init__(self, num, name):
        self.num = num
        self.name = name


#전체 Select
def select_all():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='service', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = "select * from test"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)
    finally:
        conn.close()


#DB Insert
def insert_test(test_obj):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='service', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'insert into test values(%s, %s)'
            curs.execute(sql, (test_obj.num, test_obj.name))
        conn.commit()
    finally:
        conn.close()

#DB Update
def update_test(test_obj):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='service', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'update test set name=%s where num=%s'
            curs.execute(sql, (test_obj.name, test_obj.num))
        conn.commit()
    finally:
        conn.close()


def insert_excel_to_db():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='service', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'insert into test values(%s, %s)'

            wb = load_workbook('ran70\Documents\Service_proj01\flask\templates\주식데이터.xlsx', data_only=True)
            ws = wb['Sheet']

            iter_rows = iter(ws.rows)
            next(iter_rows)
            for row in iter_rows:
                curs.execute(sql, (row[0].value, row[1].value))
            conn.commit()
    finally:
        conn.close()
        wb.close()


if __name__ == "__main__":
    insert_excel_to_db()
    select_all()

