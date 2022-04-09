import re
import time

from flask import Flask, jsonify, request

from main.mysql_operate import db
from main.md5 import get_md5
from main.redis_operate import redis_db

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
    sex = request.json.get("sex", "").strip()
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
        elif not (sex == "0" or sex == "1" or sex == ""):
            return jsonify({"data": [], "meta": {"msg": "性别只能为1或0", "status": "401"}})
        elif not (re.match(
                r"^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9["
                r"1|8|9]))\d{8}$",
                telephone)):
            return jsonify({"data": [], 'meta': {"msg": "手机号格式不正确", "status": 401}})
        elif res2:
            return jsonify({"data": [], 'meta': {"msg": "手机号已经被注册", "status": 401}})
        else:
            password = get_md5(username, password)  # 把传入的明文密码通过MD5加密变为密文，然后再进行注册
            # 有sex
            if sex != "":
                sql_success = "INSERT INTO user(username, password, sex, telephone, address) " \
                              "VALUES('{}', '{}', '{}', '{}', '{}')".format(username, password, sex, telephone,
                                                                            address)
            #  无sex
            else:
                sql_success = "INSERT INTO user(username, password, telephone, address) " \
                              "VALUES('{}', '{}', '{}', '{}')".format(username, password, telephone,
                                                                      address)
            db.execute_db(sql_success)
            # 注册不需要role角色
            registerInfo = {"username": username, "password": password, "sex": sex,
                            "telephone": telephone, "address": address}
            print("新增用户信息SQL ==>> {}".format(registerInfo))
            return jsonify({"data": registerInfo, "meta": {'msg': "注册成功", "status": 200}})
    else:
        return jsonify({"data": [], "meta": {"msg": "用户名/密码/手机号不能为空", 'status': 401}})


@app.route("/login", methods=['POST'])
def user_login():
    """登录用户"""
    username = request.json.get("username", "").strip()
    password = request.json.get("password", "").strip()
    if username and password:
        sql1 = "SELECT username FROM user WHERE username = '{}'".format(username)
        res1 = db.select_db(sql1)
        print("查询到用户名 ==>> {}".format(res1))
        if not res1:
            return jsonify({'data': [], 'meta': {'str': "用户名不存在", 'status': 401}})
        md5_password = get_md5(username, password)  # 把传入的明文密码通过MD5加密变为密文
        sql2 = "SELECT * FROM user WHERE username = '{}' and password = '{}'".format(username, md5_password)
        res2 = db.select_db(sql2)
        print("获取 {} 用户信息 == >> {}".format(username, res2))
        if res2:
            timeStamp = int(time.time())  # 获取当前时间戳
            # token = "{}{}".format(username, timeStamp)
            token = get_md5(username, str(timeStamp))  # MD5加密后得到token
            redis_db.handle_redis_token(username, token)  # 把token放到redis中存储
            login_info = {  # 构造一个字段，将 id/username/token/login_time 返回
                "id": res2[0]["id"],
                "username": username,
                "token": token,
                "login_time": time.strftime("%Y/%m/%d %H:%M:%S")
            }
            return jsonify({"data": login_info, "meta": {"msg": "成功登录", 'status': 200}})
        return jsonify({"data": [], "meta": {"msg": "用户名或密码错误", 'status': 401}})
    else:
        return jsonify({"data": [], "meta": {"msg": "用户名和密码不能为空", 'status': 401}})


@app.route("/users/admin/update/<int:id>", methods=['PUT'])
def user_update(id):
    """修改用户信息"""
    admin_user = request.json.get("admin_user", "").strip()  # 当前登录的管理员用户
    token = request.json.get("token", "").strip()  # token口令
    new_password = request.json.get("password", "").strip()  # 新的密码
    new_sex = request.json.get("sex", "0").strip()  # 新的性别，如果参数不传sex，那么默认为0(男性)
    new_telephone = request.json.get("telephone", "").strip()  # 新的手机号
    new_address = request.json.get("address", "").strip()  # 新的联系地址，默认为空串
    if admin_user and token and new_password and new_telephone:
        if not (new_sex == "0" or new_sex == "1"):
            return jsonify({"msg": "输入的性别只能是 0(男) 或 1(女)！！！", "status": 401})
        elif not (re.match(
                r"^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9["
                r"1|8|9]))\d{8}$",
                new_telephone)):
            return jsonify({"status": 401, "msg": "手机号格式不正确！！！"})
        else:
            redis_token = redis_db.handle_redis_token(admin_user)  # 从redis中取token
            if redis_token:
                if redis_token == token:  # 如果从redis中取到的token不为空，且等于请求body中的token
                    sql1 = "SELECT role FROM user WHERE username = '{}'".format(admin_user)
                    res1 = db.select_db(sql1)
                    print("根据用户名 【 {} 】 查询到用户类型 == >> {}".format(admin_user, res1))
                    user_role = res1[0]["role"]
                    if user_role == 0:  # 如果当前登录用户是管理员用户
                        sql2 = "SELECT * FROM user WHERE id = '{}'".format(id)
                        res2 = db.select_db(sql2)
                        print("根据用户ID 【 {} 】 查询到用户信息 ==>> {}".format(id, res2))
                        sql3 = "SELECT telephone FROM user WHERE telephone = '{}'".format(new_telephone)
                        res3 = db.select_db(sql3)
                        print("返回结果：{}".format(res3))
                        print("查询到手机号 ==>> {}".format(res3))
                        if not res2:  # 如果要修改的用户不存在于数据库中，res2为空
                            return jsonify({"code": 401, "msg": "修改的用户ID不存在，无法进行修改，请检查！！！"})
                        elif res3:  # 如果要修改的手机号已经存在于数据库中，res3非空
                            return jsonify({"code": 401, "msg": "手机号已被注册，无法进行修改，请检查！！！"})
                        else:
                            # 如果请求参数不传address，那么address字段不会被修改，仍为原值
                            if not new_address:
                                new_address = res2[0]["address"]
                            # 把传入的明文密码通过MD5加密变为密文
                            new_password = get_md5(res2[0]["username"], new_password)
                            sql3 = "UPDATE user SET password = '{}', sex = '{}', telephone = '{}', address = '{}' " \
                                   "WHERE id = {}".format(new_password, new_sex, new_telephone, new_address, id)
                            db.execute_db(sql3)
                            print("修改用户信息SQL ==>> {}".format(sql3))
                            return jsonify({"code": 0, "msg": "恭喜，修改用户信息成功！"})
                    else:
                        return jsonify({"status": 401, "msg": "当前用户不是管理员用户，无法进行操作，请检查！！！"})
    else:
        return jsonify({"data": [], "meta": {'msg': "管理员用户/token/密码/手机号不能为空", "status": 401}})


@app.route("/users/update/<string:username>", methods=['PUT'])
def user_update(username):
    """修改用户信息"""
    token = request.json.get("token", "").strip()  # token口令
    new_username = request.json.get("username", "").strip()
    new_password = request.json.get("password", "").strip()  # 新的密码
    new_sex = request.json.get("sex", "0").strip()  # 新的性别，如果参数不传sex，那么默认为0(男性)
    new_telephone = request.json.get("telephone", "").strip()  # 新的手机号
    new_address = request.json.get("address", "").strip()  # 新的联系地址，默认为空串
    if token and new_username and new_password and new_telephone:
        if not (new_sex == "0" or new_sex == "1"):
            return jsonify({"msg": "输入的性别只能是 0(男) 或 1(女)！！！", "status": 401})
        elif not (re.match(
                r"^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9["
                r"1|8|9]))\d{8}$",
                new_telephone)):
            return jsonify({"status": 401, "msg": "手机号格式不正确！！！"})
        else:
            redis_token = redis_db.handle_redis_token(username)  # 从redis中取token
            if redis_token == token:  # 等于请求body中的token
                new_password = get_md5(username, new_password)
                sql = "UPDATE user SET " \
                      "`username` = '{}' `password` = '{}', `sex` = '{}', `telephone` = '{}', `address` = '{}' " \
                      "WHERE username = {}".format(new_username, new_password, new_sex,
                                                   new_telephone, new_address, username)
                db.execute_db(sql)
                print("修改用户信息SQL ==>> {}".format(sql))
                return jsonify({"status": 200, "msg": "恭喜，修改用户信息成功！"})
            else:
                return jsonify({"msg": "登录状态错误", "status": 401})
    else:
        return jsonify({"data": [], "meta": {'msg': "/token/新用户名/密码/手机号不能为空", "status": 401}})


@app.route("/users/delete/<string:username>", methods=['DELETE'])
def user_delete(username):
    return
