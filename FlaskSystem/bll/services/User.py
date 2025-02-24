from utils.MySQLChain import *
def get_user_info():
    with MySQLChain(
        host='10.10.116.210',
        user='root',
        password='Password123$',
        database='student_evaluation'
    ) as db:
        result = db.table('tb_user')\
            .select()\
            .execute()
        return result


print(get_user_info())
