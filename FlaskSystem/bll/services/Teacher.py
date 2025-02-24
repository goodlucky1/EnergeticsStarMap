"""
用视图查看数据
"""
from utils.MySQLChain import *
def get_teacher_info():
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('teachers')\
            .select('teacher_id,name,gender,department_name')\
            .execute()
        return result
def get_table():
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_metrics')\
            .select('metrics_name')\
            .execute()
        return result


print(get_table())
def create_sql(*args):
    sql = 'select '
    sql+=','.join(args)
    return sql

print(create_sql('学号','姓名','爱国爱校','诚信守信'))
"""
select
null `列1`,
null `列2`
｛
'姓名':'',

｝

"""