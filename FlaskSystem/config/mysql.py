import pymysql

# 数据库配置信息
DB_CONFIG = {
    'host': '10.10.116.210',  # 数据库主机地址
    'port': 3306,         # 数据库端口号
    'user': 'root',       # 数据库用户名
    'password': 'Password123$', # 数据库密码
    'db': 'db',   # 数据库名称
    'charset': 'utf8mb4', # 字符集
    'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的游标
}

tables={
    "user":"users", #用户表
    "usertype":["管理员","教师","学生"], #学生类型
    "userrole":{"管理员":100,"教师":10,"学生":1},#用户权限
    "defaulttype":"教师", #默认用户类型
    "canreviserole":100 , #可以修改权限的权限等级
    "canrevisestudentdata":10, #可以修改学生数据的权限等级
    "getdata":{100:1,10:1,1:0} #获取数据的权限等级  10全部获取  1获取自身
}


def get_db_connection():
    """
    获取数据库连接
    :return: 数据库连接对象
    """
    connection = pymysql.connect(**DB_CONFIG)
    return connection

def execute_query(query, params=None):
    """
    执行数据库查询
    :param query: 查询语句
    :param params: 查询参数
    :return: 查询结果
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    change=cursor.execute(query, params)
    if query.__contains__("INSERT") or query.__contains__("UPDATE") or query.__contains__("DELETE"):
        connection.commit()
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result,change




if __name__ == '__main__':

    print(execute_query("SELECT * FROM user WHERE username = %s AND password = %s", ("123", "1234562"))
)