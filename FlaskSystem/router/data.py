import datetime
import os
import time
from config.mysql import execute_query,tables
from flask import Blueprint, request, jsonify, make_response,send_file,send_from_directory

"""
待完成内容

教师修改学生数据 
  暂时的请求数据-若有需要再加入
    导入
        username = request.cookies.get("username")
        studentdata = request.get_json().get("studata")  格式暂时是[{},{}]
        teachername = request.get_json().get("teachername")
    增加
        username = request.cookies.get("username")
        studentdata = request.get_json().get("studata")  格式暂时是{}
        teachername = request.get_json().get("teachername")
    修改
        username = request.cookies.get("username")
        studentdata = request.get_json().get("studata")  格式暂时是{}
        teachername = request.get_json().get("teachername")
    批量删除
        username = request.cookies.get("username")
        studentdata = request.get_json().get("studata")  格式暂时是[{},{}]
        teachername = request.get_json().get("teachername")
    删除
        username = request.cookies.get("username")
        studentdata = request.get_json().get("studata")  格式暂时是{}
        teachername = request.get_json().get("teachername")
    
    学生获取数据
        username = request.cookies.get("username")
        studentname = request.get_json().get("studentname")
    教师获取数据
        username = request.cookies.get("username")
        teachername=request.get_json().get("teachername")
  
  返回格式
    暂时是(res 修改的数据内容,change 修改的数据条数)-也可进行更改
    
    获取数据的返回格式 (res 获取的数据,istrue 是否获取成功)


教师以文件形式导入  
    参数-有需要再加入
        文件路径
    返回是否添加成功-或者其他内容
"""


file_bp = Blueprint('file', __name__, url_prefix='/file')
data_bp = Blueprint('data', __name__, url_prefix='/data')

@file_bp.route('upload', methods=['POST'])
def upload():
    username=request.cookies.get("username")

    file = request.files.get("files")
    timestamp= int(datetime.datetime.timestamp(datetime.datetime.now()))

    if not os.path.exists(fr"data\{username}\{file.filename.split('.')[0]}"):
        os.makedirs(f"data\\{username}\\{file.filename.split('.')[0]}")


    print(file.filename.split(".")[0],timestamp)
    with open(f"data\\{username}\\{file.filename.split(".")[0]}\\{timestamp}.{file.filename.split(".")[1]}","wb") as f:
        #将file保存
        f.write(file.stream.read())


    data={
        "code":200,
        "msg":"上传成功,文件已经保存于服务器",
    }
    response=make_response(jsonify(data),200)
    return response

#计算目录大小
def get_size(path):
    sizesum = 0

    if os.path.isfile(path):
        return os.path.getsize(path)

    else:
        filearr=os.listdir(path)

        for file in filearr:
          if os.path.isdir(path):
              sizesum+=get_size(os.path.join(path,file))
          else:
              sizesum+=os.path.getsize(os.path.join(path,file))

        return sizesum

@file_bp.route("list",methods=["GET"])
def file_list():
    print("username")
    username=request.cookies.get("username")

    if not os.path.exists(fr"data\{username}"):
        os.makedirs(f"data\\{username}")
        data={
            "code":200,
            "msg":"你还没有上传过文件"
        }
        response=make_response(jsonify(data),200)
        return response

    files=os.listdir(f"data\\{username}")
    filessize=[]
    for file in files:
        filessize.append(get_size(os.path.join(f"data\\{username}",file)))

    #将files与filessize组合为字典
    files=dict(zip(files,filessize))

    data={
        "code":200,
        "msg":"文件列表",
        "files":files
    }
    response=make_response(jsonify(data),200)
    return response

@file_bp.route("download",methods=["POST"])
def download():
    username=request.cookies.get("username")
    #完成文件下载,请求的数据有cookie的username-用于确认是data下的那个目录 file-文件名-这里对应确认的目录下边的目录，因为之前这个文件较大可能会切片保存  然后如果只有一个文件那么就直接返回，否则将目录压缩为压缩包再返回
    file=request.get_json().get("filename")


    if not os.path.exists(f"data\\{username}\\{file}"):
        data={
            "code":404,
            "msg":"文件不存在"
        }
        response=make_response(jsonify(data),200)
        return response

    else:
        #获取文件名称
        filearr=os.listdir(f"data\\{username}\\{file}")
        print(filearr)
        return send_from_directory(f"data\\{username}\\{file}",filearr[0],as_attachment=True)


@file_bp.route("test",methods=["GET"])
def test():
    return send_file(r"data\test\数据成绩汇总\1740055747.xlsx",as_attachment=True)


@data_bp.route("import",methods=["POST"])
def import_data():
    username = request.cookies.get("username")
    userrole = request.cookies.get("token")

    studentdata = request.get_json().get("studata")
    teachername = request.get_json().get("teachername")

    #暂认为studentdata为[{},{}]的格式
    studentdata= list(studentdata)
    print(studentdata.__len__())

    #调用学生数据导入函数

    #todo模拟返回内容
    (res,change) = ([],0)

    if change == 0:
        data={
            "code":401,
            "msg":"数据导入失败,或者该批数据已经被导入"
        }
        response=make_response(jsonify(data),200)
        return response
    elif change == studentdata.__len__():
        data={
            "code":200,
            "msg":"数据导入成功"
        }
        response=make_response(jsonify(data),200)
        return response
    elif change < studentdata.__len__():
        data={
            "code":201,
            "msg":"数据导入成功,但是可能有数据冲突发生"
        }
        response=make_response(jsonify(data),200)
        return response

    pass

@data_bp.route("add",methods=["POST"])
def add():
    username=request.cookies.get("username")
    userrole=request.cookies.get("token")

    studentdata=request.get_json().get("studata")
    teachername=request.get_json().get("teachername")

    canaddstudentdata=tables.get("canaddstudentdata")
    if userrole < canaddstudentdata:
        data={
            "code":403,
            "msg":"权限不足"
        }
        response=make_response(jsonify(data),200)
        return response
    else:
        #todo调用添加数据的函数

        #todo模拟返回内容
        (res,change) = ([],0)
        if change == 0:
            data={
                "code":401,
                "msg":"数据添加失败,或者该数据已经存在"
            }
            response=make_response(jsonify(data),200)
            return response
        elif change ==1:
            data={
                "code":200,
                "msg":"数据添加成功"
            }
            response=make_response(jsonify(data),200)
            return response
        pass

@data_bp.route("revise",methods=["POST"])
def revise():
    username=request.cookies.get("username")
    userrole=request.cookies.get("token")

    studentdata=request.get_json().get("studata")
    teachername=request.get_json().get("teachername")

    canrevisestudentdata=tables.get("canrevisestudentdata")

    if userrole < canrevisestudentdata:
        data={
            "code":403,
            "msg":"权限不足"
        }
        response=make_response(jsonify(data),200)
        return response

    else:
        #todo调用修改数据的函数

        #todo模拟返回内容
        (res,change) = ([],0)
        if change == 0:
            data={
                "code":401,
                "msg":"数据修改失败,或者该数据已经不存在"
            }
            response=make_response(jsonify(data),200)
            return response
        elif change ==1:
            data={
                "code":200,
                "msg":"数据修改成功"
            }
            response=make_response(jsonify(data),200)
            return response

@data_bp.route("deletesimple",methods=["POST"])
def deletesimple():
    username=request.cookies.get("username")
    userrole=request.cookies.get("token")

    studentdata=request.get_json().get("studata")
    teachername=request.get_json().get("teachername")

    candeletestudentdata=tables.get("candeletestudentdata")

    if userrole < candeletestudentdata:
        data={
            "code":403,
            "msg":"权限不足"
        }
        response=make_response(jsonify(data),200)
        return response
    else:
        #todo调用删除数据的函数

        #todo模拟返回内容
        (res,change) = ([],0)
        if change == 0:
            data={
                "code":401,
                "msg":"数据删除失败,或者该批数据已经不存在"
            }
            response=make_response(jsonify(data),200)
            return response
        elif change == list(studentdata).__len__():
            data={
                "code":200,
                "msg":"数据删除成功"
            }
            response = make_response(jsonify(data), 200)
            return response

        elif change < list(studentdata).__len__():
            data={
                "code":201,
                "msg":"数据删除成功,但是可能有数据并不存在"
            }
            response=make_response(jsonify(data),200)
            return response

@data_bp.route("delete",methods=["POST"])
def delete():
    username=request.cookies.get("username")
    userrole=request.cookies.get("token")

    studentdata=request.get_json().get("studata")
    teachername=request.get_json().get("teachername")

    candeletestudentdata=tables.get("candeletestudentdata")

    if userrole < candeletestudentdata:
        data={
            "code":403,
            "msg":"权限不足"
        }
        response=make_response(jsonify(data),200)
        return response
    else:
        #todo调用删除数据的函数

        #todo模拟返回内容
        (res,change) = ([],0)
        if change == 0:
            data={
                "code":401,
                "msg":"数据删除失败,或者该数据已经不存在"
            }
            response=make_response(jsonify(data),200)
            return response
        elif change == 1:
            data={
                "code":200,
                "msg":"数据删除成功"
            }
            response = make_response(jsonify(data), 200)
            return response


@data_bp.route("getdata",methods=["POST"])
def getdata():
    username=request.cookies.get("username")
    userrole=request.cookies.get("token")

    getdatalevel=tables.get("getdata").get(userrole)
    if getdatalevel == 1:

        studentname=request.get_json().get("studentname")

        #todo调用获取数据的函数

        #todo模拟返回内容
        (res,change)=([],0)
        if change == 0:
            data={
                "code":401,
                "msg":"数据获取失败,或者该数据不存在"
            }
            response=make_response(jsonify(data),200)
            return response
        elif change == 1:
            data={
                "code":200,
                "msg":"数据获取成功",
                "data": res
            }
            response=make_response(jsonify(data),200)
            return response
    elif getdatalevel == 1:

        teachername=request.get_json().get("teachername")
        #todo调用获取数据的函数
        #todo模拟返回内容
        (res,change)=([],0)
        if change == 0:
            data={
                "code":401,
                "msg":"数据获取失败,或者该数据不存在"
            }
            response=make_response(jsonify(data),200)
            return response
        elif change != 0:
            data={
                "code":200,
                "msg":"数据获取成功",
                "data":res
            }
            response=make_response(jsonify(data),200)
            return response






