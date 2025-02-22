import datetime
import os
import time
from config.mysql import execute_query,tables
from flask import Blueprint, request, jsonify, make_response,send_file,send_from_directory

evaluation_bp = Blueprint('evaluation', __name__, url_prefix='/evaluation')

#获取评价维度
@evaluation_bp.route("getdimension",methods=["GET"])
def getdimension():
    pass

#获取评价指标
@evaluation_bp.route("getindicator",methods=["GET"])
def getindicator():
    pass

#修改评价体系或指标
@evaluation_bp.route("revisepj",methods=["POST"])
def revisepj():
    pass

#获取评价结果
@evaluation_bp.route("getevaluation",methods=["GET"])
def getevaluation():
    pass








# from flask import Blueprint, request, jsonify
# from ..models import Indicator, Evaluation  # 假设你有 Indicator 和 Evaluation 模型
# from ..utils import validate_input  # 假设你有一个工具函数用于验证输入
#
# evaluation_bp = Blueprint('evaluation', __name__)
#
# # 假设有一个存储评价维度和指标的字典
# evaluation_metrics = {
#     "dimensions": [],
#     "indicators": []
# }
#
# @evaluation_bp.route('/dimensions', methods=['POST'])
# def add_dimension():
#     dimension = request.json
#     evaluation_metrics['dimensions'].append(dimension)
#     return jsonify({"message": "Dimension added successfully"}), 201
#
# @evaluation_bp.route('/dimensions/<int:dimension_id>', methods=['DELETE'])
# def delete_dimension(dimension_id):
#     if dimension_id >= len(evaluation_metrics['dimensions']):
#         return jsonify({"message": "Dimension not found"}), 404
#     evaluation_metrics['dimensions'].pop(dimension_id)
#     return jsonify({"message": "Dimension deleted successfully"})
#
# @evaluation_bp.route('/indicators', methods=['POST'])
# def add_indicator():
#     indicator = request.json
#     evaluation_metrics['indicators'].append(indicator)
#     return jsonify({"message": "Indicator added successfully"}), 201
#
# @evaluation_bp.route('/indicators/<int:indicator_id>', methods=['GET'])
# def get_indicator(indicator_id):
#     indicator = Indicator.query.get_or_404(indicator_id)
#     return jsonify(indicator.to_dict())
#
# @evaluation_bp.route('/evaluate', methods=['POST'])
# def evaluate():
#     data = request.json
#     if not validate_input(data, ['student_id', 'indicator_id', 'score']):
#         return jsonify({"error": "Invalid input"}), 400
#
#     evaluation = Evaluation(
#         student_id=data['student_id'],
#         indicator_id=data['indicator_id'],
#         score=data['score']
#     )
#     evaluation.save()
#     return jsonify({"message": "Evaluation submitted successfully"}), 201
#
# @evaluation_bp.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Resource not found"}), 404
#
# @evaluation_bp.errorhandler(500)
# def internal_error(error):
#     return jsonify({"error": "Internal server error"}), 500

