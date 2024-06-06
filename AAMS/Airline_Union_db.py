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
                               database = C.DB_NAME, charset = 'utf8mb4')
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

# 04 创建购票用户函数
def create_user(cid, cname, realname, telephonenum, csid, csex, password):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    try:
        encrypted_password = md5(password)
        cur.execute(
            "INSERT INTO Customers (CID, Cname, Realname, TelephoneNum, Csid, Csex, Password) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (cid, cname, realname, telephonenum, csid, csex, encrypted_password)
        )
        conn.commit()
    except pymysql.IntegrityError:
        cur.close()
        return False
    cur.close()
    return True

# 05 验证购票用户函数
def validate_user(cid, password):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    encrypted_password = md5(password)
    cur.execute("SELECT * FROM Customers WHERE CID = %s AND Password = %s", (cid, encrypted_password))
    user = cur.fetchone()
    cur.close()
    return user is not None

# 06 验证航司管理员函数
def validate_flight_manager(fmid, password):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    encrypted_password = md5(password)
    cur.execute("SELECT * FROM FlightsManagers WHERE FMID = %s AND Fpassword = %s", (fmid, encrypted_password))
    user = cur.fetchone()
    cur.close()
    return user is not None

# 07 验证机场管理员函数
def validate_Airport_manager(amid, password):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    encrypted_password = md5(password)
    cur.execute("SELECT * FROM AirportsManagers WHERE AMID = %s AND AMpassword = %s", (amid, encrypted_password))
    user = cur.fetchone()
    cur.close()
    return user is not None


# 08 显示购票用户信息到不同QLineEdit文本框的方法
def get_user_info(cid):
    sql = f"SELECT CID, Cname, Realname, TelephoneNum, Csid, Csex FROM Customers WHERE CID = '{cid}'"
    result = sql_execute(sql)
    if result:
        return result[0]  # 假设CID是唯一的，只会返回一行结果
    return None

def update_user_info(user_info):
    try:
        # 构建更新用户信息的 SQL 语句
        sql = f"""
            UPDATE Customers
            SET Cname = '{user_info['Cname']}', Realname = '{user_info['Realname']}', 
                TelephoneNum = '{user_info['TelephoneNum']}', Csid = '{user_info['Csid']}', 
                Csex = '{user_info['Csex']}'
        """

        # 如果新密码不为空，则更新密码
        if user_info['NewPassword']:
            sql += f", Password = '{md5(user_info['NewPassword'])}'"

        sql += f" WHERE CID = '{user_info['CID']}'"

        # 执行 SQL 语句
        sql_execute(sql)
        conn.commit()  # 提交事务
        return True
    except Exception as e:
        print("Error in update_user_info:", e)
        conn.rollback()  # 发生错误时回滚事务
        return False


def get_airports_from_db():
    sql = "SELECT City, Aname FROM Airports"
    return sql_execute(sql)

def search_flights(departure_airport, arrival_airport, selected_date):
    sql = """
        SELECT FlightsID, DeparturePlace, ArrivalPlace, DepartureAirport, ArrivalAirport, Departuredate, 
        Takeofftime, TotalTime, PlantType, Fprice
        FROM Flights    
        WHERE DepartureAirport = '{}' AND ArrivalAirport = '{}' AND Departuredate = '{}'
    """.format(departure_airport, arrival_airport, selected_date)

    return sql_execute(sql)


# 加密示例
if __name__ == '__main__':
    str_md5 = md5("1002")
    print('MD5加密后为：' + str_md5)


if __name__ == "__main__":
    # 测试 get_user_info 函数
    user_info = get_user_info('LFNL')  # 替换为实际用户ID
    if user_info:
        print("User info retrieved:", user_info)
    else:
        print("User not found")