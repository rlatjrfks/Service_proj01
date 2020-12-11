import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook

def insert_excel_to_db():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='service', charset='utf8')
    try:
        with conn.cursor() as curs:
            sql = 'insert into jongmok_list values(%s, %s)'

            wb = load_workbook("/Users/ran70/Documents/Service_proj01/flask/templates/주식데이터.xlsx", data_only=True)
            ws = wb['Sheet']

            iter_rows = iter(ws.rows)
            next(iter_rows)
            for row in iter_rows:

                curs.execute(sql, (row[0].value, row[1].value))
            conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    insert_excel_to_db()
