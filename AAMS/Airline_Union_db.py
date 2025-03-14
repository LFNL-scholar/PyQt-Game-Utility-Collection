"""
项目名称：Airline Alliance Management System 航空联盟管理系统
作者：LFNL_Scholar
时间：2024/6
代码功能：数据库链接与交互
"""

import pymysql
import hashlib

import random
import datetime

import traceback  # 导入用于输出详细异常信息的模块

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


def get_airline_info(fmid):
    try:
        sql = f"SELECT Fname, Fsex, FMID FROM FlightsManagers WHERE FMID = '{fmid}'"
        result = sql_execute(sql)
        if result:
            return result[0]  # 假设FMID是唯一的，只会返回一行结果
        return None
    except Exception as e:
        print("Error in get_airline_info:", e)
        return None


def update_airline_info(user_info):
    try:
        # 构建更新用户信息的 SQL 语句
        sql = f"""
            UPDATE FlightsManagers
            SET Fname = '{user_info['Fname']}', 
                Fsex = '{user_info['Fsex']}'
        """

        # 如果新密码不为空，则更新密码
        if user_info['NewPassword']:
            sql += f", Fpassword = '{md5(user_info['NewPassword'])}'"

        sql += f" WHERE FMID = '{user_info['FMID']}'"

        # 执行 SQL 语句
        sql_execute(sql)
        conn.commit()  # 提交事务
        return True
    except Exception as e:
        print("Error in update_airline_info:", e)
        conn.rollback()  # 发生错误时回滚事务
        return False


def update_airport_manager_info(user_info):
    try:
        # 构建更新用户信息的 SQL 语句
        sql = f"""
            UPDATE AirportsManagers
            SET AMname = '{user_info['AMname']}', 
                AMsex = '{user_info['AMsex']}'
        """

        # 如果新密码不为空，则更新密码
        if user_info['NewPassword']:
            sql += f", AMpassword = '{md5(user_info['NewPassword'])}'"

        sql += f" WHERE AMID = '{user_info['AMID']}'"

        # 执行 SQL 语句
        sql_execute(sql)
        conn.commit()  # 提交事务
        return True
    except Exception as e:
        print("Error in update_airport_manager_info:", e)
        conn.rollback()  # 发生错误时回滚事务
        return False

def get_airport_manager_info(amid):
    try:
        sql = f"SELECT AMname, AMsex, AMID FROM AirportsManagers WHERE AMID = '{amid}'"
        result = sql_execute(sql)
        if result:
            return result[0]  # 假设AMID是唯一的，只会返回一行结果
        return None
    except Exception as e:
        print("Error in get_airport_manager_info:", e)
        return None


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

# 根据机场名搜索对应的航班
def search_Airport_flights(departure_airport):
    sql = """
        SELECT FlightsID, DeparturePlace, ArrivalPlace, DepartureAirport, ArrivalAirport, Departuredate, 
        Takeofftime, TotalTime, PlantType
        FROM Flights    
        WHERE DepartureAirport = '{}'
    """.format(departure_airport)

    return sql_execute(sql)


# 根据机场管理员账号查询机场名的函数
def search_aname_by_amid(cid):
    sql = """
        SELECT Aname
        FROM AirportsManagers
        WHERE AMID = '{}'
    """.format(cid)
    result = sql_execute(sql)
    if result:
        return result[0][0]
    else:
        return None




# 0 插入乘客信息函数
def insert_passenger(order_id, psid, pname, psex):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Passengers (Order_ID, PSid, Pname, Psex) VALUES (%s, %s, %s, %s)",
            (order_id, psid, pname, psex)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()  # 回滚事务
        cur.close()
        raise e
    cur.close()
    return True




# 0 插入机票信息函数
def insert_ticket(flights_id, seat_num, orders_id, psid, ticket_price):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Tickets (FlightsID, SeatNum, OrdersID, PSid, TicketPrice) VALUES (%s, %s, %s, %s, %s)",
            (flights_id, seat_num, orders_id, psid, ticket_price)
        )
        conn.commit()
    except pymysql.IntegrityError:
        cur.close()
        return False
    cur.close()
    return True

# 0 生成订单编号
def generate_order_id():
    return 'AC' + ''.join(random.choices('0123456789', k=10))

# 0 插入订单信息函数
def insert_order(order_id, flightID,  pay, status, payment_time, cid):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Orders (OrdersID, FlightsID, Pay, Status, PaymentTime, CID) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (order_id, flightID, pay, status, payment_time, cid)
        )
        conn.commit()
    except pymysql.IntegrityError:
        cur.close()
        return False
    cur.close()
    return True

# 搜索订单数据
def search_orders(cid):
    sql = """
        SELECT OrdersID, FlightsID, Pay, Status, PaymentTime FROM Orders    
        WHERE CID = '{}'
    """.format(cid)

    return sql_execute(sql)


def search_sid(cid):
    sql = """
        SELECT Csid FROM Customers   
        WHERE CID = '{}'
    """.format(cid)

    result = sql_execute(sql)
    if result:
        return result[0][0]  # 返回查询结果的第一个行的第一个列的值，即身份证号码
    else:
        return None  # 如果没有找到记录，返回None或者适合的默认值


# 根据身份证号查询机票的函数
def search_tickets_by_sid(csid):
    sql = """
        SELECT *
        FROM Tickets
        WHERE PSid = '{}'
    """.format(csid)

    return sql_execute(sql)



def delete_order(order_id):
    try:
        # 开始事务
        sql_begin_transaction = "START TRANSACTION"
        sql_execute(sql_begin_transaction)

        # 删除 Tickets 表中的数据
        sql_delete_tickets = "DELETE FROM Tickets WHERE OrdersID = '{}'".format(order_id)
        sql_execute(sql_delete_tickets)
        print(f"Deleted tickets for order {order_id}")

        # 删除 Passengers 表中的数据
        sql_delete_passengers = "DELETE FROM Passengers WHERE Order_ID = '{}'".format(order_id)
        sql_execute(sql_delete_passengers)
        print(f"Deleted passengers for order {order_id}")

        # 删除 Orders 表中的订单数据
        sql_delete_orders = "DELETE FROM Orders WHERE OrdersID = '{}'".format(order_id)
        sql_execute(sql_delete_orders)
        print(f"Deleted order {order_id}")

        # 提交事务
        sql_commit_transaction = "COMMIT"
        sql_execute(sql_commit_transaction)

    except Exception as e:
        # 回滚事务
        sql_rollback_transaction = "ROLLBACK"
        sql_execute(sql_rollback_transaction)

        # 输出异常信息
        traceback.print_exc()
        raise RuntimeError(f"Error deleting order {order_id}: {str(e)}")


def get_realname_from_database(cid):
    try:
        # 构造查询语句
        sql = """
            SELECT Realname FROM Customers
            WHERE CID = '{}'
        """.format(cid)

        # 执行查询并获取结果
        result = sql_execute(sql)

        # 检查是否有结果
        if result:
            return result[0][0]  # 返回查询结果的第一个行的第一个列的值，即真实姓名
        else:
            return "Unknown"  # 如果没有找到记录，返回适当的默认值，例如 "Unknown"

    except Exception as e:
        # 输出异常信息（可选）
        print(f"Error retrieving realname for CID {cid}: {str(e)}")
        return "Unknown"  # 返回默认值或者适当的错误处理方式


# 根据身份证号查询机票和航班信息
def search_info_by_sid(csid):
    sql = """
        SELECT t.FlightsID, f.DeparturePlace, f.ArrivalPlace, f.DepartureAirport, 
               f.ArrivalAirport, f.Departuredate, 
               TIME_FORMAT(f.Takeofftime, '%H:%i:%s') AS Takeofftime, 
               TIME_FORMAT(ADDTIME(f.Takeofftime, f.TotalTime), '%H:%i:%s') AS TotalTime, 
               t.SeatNum, f.PlantType
        FROM Tickets t
        JOIN Flights f ON t.FlightsID = f.FlightsID
        WHERE t.PSid = '{}'
    """.format(csid)
    return sql_execute(sql)


def publish_flight(flight_number, departure_city, arrival_city, departure_airport, arrival_airport, plane_type, price):
    global conn
    if conn is None:
        conn = conn_mysql()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Flights (FlightsID, DeparturePlace, ArrivalPlace, DepartureAirport, "
            "ArrivalAirport, PlantType, Fprice) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (flight_number, departure_city, arrival_city, departure_airport, arrival_airport, plane_type, price)
        )
        conn.commit()
        cur.close()
        return True
    except pymysql.IntegrityError as ie:
        conn.rollback()
        cur.close()
        print(f"IntegrityError: {ie}")
        return False
    except Exception as e:
        conn.rollback()
        cur.close()
        print(f"An error occurred: {e}")
        return False


def update_flight_details(flight_id, flight_date, departure_time, flight_time):

    try:
        sql = f"""
        UPDATE Flights
        SET Departuredate = '{flight_date}', Takeofftime = '{departure_time}', TotalTime = '{flight_time}'
        WHERE FlightsID = '{flight_id}'
        """
        sql_execute(sql)
        conn.commit()  # 提交更改
    except Exception as e:
        print(f"更新航班详情时出错: {e}")




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

if __name__ == '__main__':
    # 生成订单编号
    order_id = generate_order_id()
    payment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(order_id, payment_time)
