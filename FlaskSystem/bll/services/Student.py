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
        result = db.table('students')\
            .select()\
            .execute()
        return result
    #返回数据类型:[{},{}]
"""
删除学号
"""
def delete_student_info(student_id):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('students')\
            .deleted() \
            .where('student_id=%s', student_id) \
            .execute()
        return result
"""
批量删除
"""
def many_delete_student_info(*args):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('students')\
            .deleted() \
            .where("student_id in (%s)" % ",".join(["%s"]*len(args)),args)\
        .execute()
#获取院系信息
def get_department():
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_departments')\
            .select("department_name")\
            .execute()
        return result
#获取某院系中所有专业
def get_major(major_id):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_major')\
            .select("major_name")\
        .where("department_id=%s",major_id)\
            .execute()
        return result
#获取某专业的所有班级
def get_class(major_id):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_class')\
            .select("class_name")\
        .where("major_id=%s",major_id)\
            .execute()
        return result
#获取评价纬度
def get_dimension():
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_dimension')\
            .select("dimension_name")\
            .execute()
        return result
#获取某维度下的所有指标
def get_metric(dimension_id):
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_metrics')\
            .select("metrics_name")\
        .where("dimension_id=%s",dimension_id)\
            .execute()
        return result
def get_student_metric():
    pass

print(get_metric(2))
print(get_dimension())
print(get_class(1))
