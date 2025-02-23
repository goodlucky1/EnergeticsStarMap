"""
王烨 2025/2/23
学生信息增删改查bll
"""
from utils.MySQLChain import *
"""
获取学生信息
"""
def get_student_info():
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('VW_STUDENT_INFO')\
            .select()\
            .execute()
        return result
"""
通过名字查询数据
"""
def get_student_info_by_name(student_name):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('VW_STUDENT_INFO')\
            .select()\
            .where('student_name = %s', student_name)\
            .execute()
        return result
"""
根据学号删除学生
"""
def delete_student_by_id(student_id):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('VW_STUDENT_INFO')\
            .where('student_id = %s', student_id)\
            .deleted()\
            .execute()
        return result