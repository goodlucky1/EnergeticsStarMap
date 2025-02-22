import json

from flask import Blueprint, request, jsonify,make_response
from werkzeug.security import check_password_hash
import datetime
from config.mysql import execute_query,tables

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("login",methods=['POST'])
def login():

    # 从请求中获取用户名和密码
    username = request.get_json().get('username', None)
    password = request.get_json().get('password', None)
    # 获取用户表
    tablename=tables.get("user")


    # 执行查询
    (res,change)=execute_query(f"SELECT * FROM {tablename} WHERE username = %s AND password = %s", (username, password))
    print(res)
    if change == 1:
        data={
            "code":200,
            "message":"Login successful"
        }
        userrole = tables.get("userrole").get(dict(res[0]).get("user_type"))

        response=make_response(jsonify(data),200)
        response.set_cookie("token",str(userrole),expires=datetime.datetime.now()+datetime.timedelta(days=1))
        response.set_cookie("username", username, expires=datetime.datetime.now() + datetime.timedelta(days=1))

        return response

    else:
        data = {
            "code": 401,
            "message": "Login fail"
        }
        response = make_response(jsonify(data), 200)
        return response

@auth_bp.route("register",methods=['POST'])
def register():
    # 从请求中获取用户名和密码
    username = request.get_json().get('username', None)
    password = request.get_json().get('password', None)
    # 获取用户表
    tablename = tables.get("user")
    defaulttype = tables.get("defaulttype")
    userrole=tables.get("userrole").get(defaulttype)

    #检测用户名是否已经存在
    (res,change)=execute_query(f"SELECT * FROM {tablename} WHERE username = %s", (username,))
    if change == 1:
        data={
            "code":401,
            "message":"Username already exists"
        }

        response=make_response(jsonify(data),200)
        return response

    else:
        # 执行插入
        (res, change) = execute_query(f"INSERT INTO {tablename}(username,password,user_type) VALUES (%s,%s,%s)", (username, password,defaulttype))
        print(res,change)

        if change == 1:
            data={
                "code":200,
                "message":"Register successful"
            }
            response=make_response(jsonify(data),200)
            response.set_cookie("token",str(userrole),expires=datetime.datetime.now()+datetime.timedelta(days=1))
            response.set_cookie("username", username, expires=datetime.datetime.now() + datetime.timedelta(days=1))

            return response
        else:
            data={
                "code":402,
                "message":"An unknown issue has occurred, contact your administrator"
            }

            response=make_response(jsonify(data),200)
            return response

@auth_bp.route("revise",methods=['POST'])
def revise():
    username = request.get_json().get('username', None)

    password = request.get_json().get('password', None)
    usertype = request.get_json().get("usertype", None)

    # 获取用户表
    tablename = tables.get("user")

    #检测是否含有该用户
    (res,change)=execute_query(f"SELECT * FROM {tablename} WHERE username = %s", (username,))
    if change == 1:
        sql=f"UPDATE {tablename} SET"
        params=None

        if password is not None:
            sql+=f" password = %s"
            params=(password,)
        if usertype is not None and password is not None:
            sql+=f" ,user_type = %s"
            params+=(usertype,)
        else:
            sql+=f" user_type = %s"
            params=(usertype,)
        sql+=f" WHERE username = %s"
        params+=(username,)

        (res, change) = execute_query(sql, params)
        if change == 1:
            data={
                "code":200,
                "message":"revise successful"
            }
            response=make_response(jsonify(data),200)
            return response

        else:
            data={
                "code":402,
                "message":"An unknown issue has occurred, contact your administrator"
            }
            response=make_response(jsonify(data),200)
            return response







