import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np

def insert_excel_to_db():
    conn1 = pymysql.connect(
        host='ls-360d5e5827a35e0a46fa340307d68f5a00a3b151.cvbhe0hq8rxv.ap-northeast-2.rds.amazonaws.com', port=3306,
        user='dbmasteruser', passwd='Qa]HHh]dc1NsX>VLfo<=JA^1GcEWOCY$', db='dbmaster', charset='utf8')

    sql1 = 'delete from jongmok_list'
    cur1 = conn1.cursor()
    cur1.execute(sql1)
    conn1.commit()


    conn = pymysql.connect(
        host='ls-360d5e5827a35e0a46fa340307d68f5a00a3b151.cvbhe0hq8rxv.ap-northeast-2.rds.amazonaws.com', port=3306,
        user='dbmasteruser', passwd='Qa]HHh]dc1NsX>VLfo<=JA^1GcEWOCY$', db='dbmaster', charset='utf8')

    try:
        with conn.cursor() as curs:

            sql = 'insert into jongmok_list values(%s, %s, %s)'

            wb = load_workbook("templates/jusikdata.xlsx", data_only=True)
            ws = wb['Sheet']

            iter_rows = iter(ws.rows)
            next(iter_rows)
            for row in iter_rows:
                value = row[1].value.split(",")
                vallist = ''.join(value)
                value_float = row[2].value.split("%")
                curs.execute(sql, (row[0].value, vallist, value_float[0]))
            conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    insert_excel_to_db()
