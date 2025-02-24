from typing import List, Dict, Any

import pymysql

class MySQLChain:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self._reset_query()

    def _reset_query(self):
        """重置查询参数"""
        self.query_type = None  # 操作类型（SELECT/INSERT/UPDATE/DELETE）
        self.fields = '*'       # 查询字段
        self._table = None   # 表名
        self._limit=None
        self.where_conditions = []  # WHERE 条件列表
        self.where_params = []      # WHERE 参数列表
        self.insert_data = {}       # INSERT 数据
        self.update_data = {}
        self._batch_data=[]# UPDATE 数据
    def table(self, table_name):
        """设置表名"""
        self._table = table_name
        return self
    def connect(self):
        """连接数据库"""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
        return self

    def close(self):
        """关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self._reset_query()

    def select(self, fields='*'):
        """设置 SELECT 字段"""
        self.query_type = 'SELECT'
        self.fields = fields
        return self

    def where(self, condition, *params):
        """添加 WHERE 条件"""
        self.where_conditions.append(condition)
        self.where_params.extend(params)
        print(params)
        return self
    def limit(self, limit):
        """设置 LIMIT"""
        self._limit = limit
        return self
    def insert(self, data):
        """设置 INSERT 数据"""
        self.query_type = 'INSERT'
        self.insert_data = data
        return self

    def bulk_insert(self, data: List[Dict[str, Any]]) -> 'MySQLChain':
        """设置批量插入数据"""

        self.query_type = 'BATCH_INSERT'
        self._batch_data = data
        return self

    def _build_batch_insert_query(self) -> tuple:
        """构建批量插入 SQL 语句和参数"""

        # 获取所有键（列名）并确保一致性
        columns = list(self._batch_data[0].keys())
        for item in self._batch_data:
            if list(item.keys()) != columns:
                raise ValueError("批量插入数据的列名不一致")

        # 构建 VALUES 占位符：(%s, %s), (%s, %s)...
        placeholders = ', '.join(['(%s)' % ', '.join(['%s'] * len(columns))] * len(self._batch_data))

        # 平铺参数列表
        values = []
        for item in self._batch_data:
            values.extend(item.values())

        query = f"INSERT INTO {self._table} ({', '.join(columns)}) VALUES {placeholders}"
        return query, values
    def update(self, data):
        """设置 UPDATE 数据"""
        self.query_type = 'UPDATE'
        self.update_data = data
        return self
    def deleted(self):
        """设置 DELETE 数据"""
        self.query_type = 'DELETE'
        # self.delete_data = data
        return self


    def _build_select_query(self):
        """构建 SELECT 查询语句"""
        query = f"SELECT {self.fields} FROM {self._table}"
        if self.where_conditions:
            query += " WHERE " + " AND ".join(self.where_conditions)
        return query

    def _build_insert_query(self):
        """构建 INSERT 查询语句"""
        columns = ', '.join(self.insert_data.keys())
        placeholders = ', '.join(['%s'] * len(self.insert_data))
        query = f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders})"
        return query, list(self.insert_data.values())

    def _build_update_query(self):
        """构建 UPDATE 查询语句"""
        set_clause = ', '.join([f"{k} = %s" for k in self.update_data.keys()])
        query = f"UPDATE {self._table} SET {set_clause}"
        if self.where_conditions:
            query += " WHERE " + " AND ".join(self.where_conditions)
        params = list(self.update_data.values()) + self.where_params
        return query, params
    def _build_delete_query(self):
        """构建 DELETE 查询语句"""
        query = f"DELETE FROM {self._table}"
        if self.where_conditions:
            query += " WHERE " + " AND ".join(self.where_conditions)
            return query
    def execute(self):
        """执行查询并返回结果"""
        if not self.connection:
            raise Exception("未连接数据库，请先调用 `connect()` 方法")

        if self.query_type == 'SELECT':
            query = self._build_select_query()
            self.cursor.execute(query, self.where_params)
            return self.cursor.fetchall()

        elif self.query_type == 'INSERT':
            query, params = self._build_insert_query()
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid

        elif self.query_type == 'UPDATE':
            query, params = self._build_update_query()
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        elif self.query_type == 'DELETE':
            query = self._build_delete_query()
            self.cursor.execute(query, self.where_params)
            self.connection.commit()
            return self.cursor.rowcount
        elif self.query_type == 'BATCH_INSERT':
            query, params = self._build_batch_insert_query()
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount

        else:
            raise Exception("未指定操作类型（SELECT/INSERT/UPDATE）")

    def __enter__(self):
        """支持上下文管理器"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时关闭连接"""
        self.close()

# 示例用法
if __name__ == "__main__":
    # 使用上下文管理器自动管理连接
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        # 链式调用 SELECT 查询
        result = db.table('VW_STUDENT_INFO')\
            .select()\
        .execute()
        print(result)

        # # 链式调用 INSERT
        # new_id = db.table('users').insert({'name': 'Alice', 'age': 25}).execute()
        # print("插入的 ID:", new_id)
        #
        # # 链式调用 UPDATE
        # row_count = db.table('users').update({'age': 26}).where('id = %s', new_id).execute()
        # print("更新的行数:", row_count)

