from flask import Flask, make_response, jsonify
from router.auth import auth_bp
from router.data import data_bp,file_bp

app = Flask(__name__)

# 注册蓝本
app.register_blueprint(auth_bp)
app.register_blueprint(data_bp)
app.register_blueprint(file_bp)


#config
app.config['X_SENDFILE_TYPE'] = 'X-Accel-Redirect'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
@app.errorhandler(404)
def not_found(error):
    data={
        "code":404,
        "message":"Resource not found"
    }
    response=make_response(jsonify(data),404)
    return response

@app.errorhandler(500)
def internal_error(error):
    data={
        "code":500,
        "message":"Internal server error"
    }
    response=make_response(jsonify(data),500)
    return response



if __name__ == '__main__':
    app.run()
