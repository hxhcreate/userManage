from flask import Flask, jsonify, request
from main.mysql_operate import db
import re, time

app = Flask(__name__)
app.config.from_object('appConfig')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/users", methods=['GET'])
def get_all_user():
    sql = " select * from `user` "
    data = db.select_db(sql)
    print("获取所有的用户信息 == >> {}".format(data))
    return jsonify({"data": data, "msg": "查询成功"})
