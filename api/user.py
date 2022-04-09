from flask import Flask, jsonify, request

from main.mysql_operate import db
import re

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/users", methods=['GET'])
def get_all_user():
    sql = " select * from `user` "
    data = db.select_db(sql)
    print("获取所有的用户信息 == >> {}".format(data))
    return jsonify({"data": data, "meta": {"msg": "查询成功", "status": 200}})


@app.route("/users/<string:username>", methods=["GET"])
def get_user(username):
    """获取某个用户信息"""
    sql = "SELECT * FROM `user` WHERE username = '{}'".format(username)
    data = db.select_db(sql)
    print("获取 {} 用户信息 == >> {}".format(username, data))
    if data:
        return jsonify({"data": data, "meta": {"msg": "查询成功", "status": 200}})
    return jsonify({"data": data, "meta": {"msg": "无法找到该用户", "status": 404}})


@app.route("/register", methods=['POST'])
def user_register():
    """注册用户"""
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    sex = request.json.get("sex", "0").strip()
    telephone = request.json.get("telephone", "").strip()
    address = request.json.get("address", "").strip()
    if username and password and telephone:
        sql1 = "select username from `user` where username = '{}'".format(username)
        res1 = db.select_db(sql1)
        print("查询到用户名 ===>> {}".format(res1))
        sql2 = "select telephone from `user` where telephone = '{}'".format(telephone)
        res2 = db.select_db(sql2)
        print("查询到手机号 ===>> {}".format(res2))
        if res1:
            return jsonify({"data": [], "meta": {"msg": "已经存在该用户名", "status": "401"}})
        elif not (sex == "0" or sex == "1"):
            return jsonify({"data": [], "meta": {"msg": "性别只能为1或0", "status": "401"}})
        elif not (re.match(
                r"^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$",
                telephone)):
            return jsonify({"data": [], 'meta': {"msg": "手机号格式不正确", "status": 401}})
        elif res2:
            return jsonify({"data": [], 'meta': {"msg": "手机号已经被注册", "status": 401}})
    else:
        return jsonify({"data": [], "meta": {"msg": "用户名/密码/手机号不能为空", 'status': 401}})
