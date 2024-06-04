"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：数据库链接与交互
"""

import pymysql
import hashlib
import Config as C

global conn
conn = None

# 01 获取数据库连接
def conn_mysql():
    conn = None
    try:
        conn = pymysql.connect(host = C.DB_HOST, port = 3306, user = C.DB_USER, password = C.DB_PASSWORD,
                               database = C.DB_NAME, charset = 'utf-8')
    except Exception as e:
        print(e)
    return conn

# 02 根据SQL语句操作数据库
def sql_execute(sql):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()  # 生成游标
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

# 03 获取MD5加密结果
def md5(text):
    text = bytes(text, encoding='utf-8')
    return hashlib.md5(text).hexdigest()

# 加密示例
if __name__ == '__main__':
    str_md5 = md5("123456")
    print('MD5加密后为：' + str_md5)
