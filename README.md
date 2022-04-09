> 练习Python 后端的初步项目 主要聚焦用户管理
>
> 将尝试不同的数据库 不同的数据库驱动
> 

### 请求接口

- 获取所有用户接口请求示例（可直接在浏览器输入栏请求）：

```
请求方式：GET
请求地址：http://127.0.0.1:9999/users
```

- 获取wintest用户接口请求示例（可直接在浏览器输入栏请求）：

```
请求方式：GET
请求地址：http://127.0.0.1:9999/users/wintest
```

- 用户注册接口请求示例：

```
请求方式：POST
请求地址：http://127.0.0.1:9999/register
请求头：
Content-Type: application/json

Body：{"username": "wintest5", "password": "123456", "sex": "1", "telephone":"13500010005", "address": "上海市黄浦区"}
```

- 用户登录接口请求示例：

```
请求方式：POST
请求地址：http://127.0.0.1:9999/login
请求头：
Content-Type: application/x-www-form-urlencoded

Body：username=wintest&password=123456
```

- 修改用户接口请求示例（ token 可以从用户登录成功后的接口返回数据中获取）：

```
请求方式：PUT
请求地址：http://127.0.0.1:9999/update/user/3
请求头：
Content-Type: application/json

Body：{"admin_user": "wintest", "token": "f54f9d6ebba2c75d45ba00a8832cb593", "sex": "1", "address": "广州市天河区", "password": "12345678", "telephone": "13500010003"}
```

- 删除用户接口请求示例（ token 可以从用户登录成功后的接口返回数据中获取）：：

```
请求方式：POST
请求地址：http://127.0.0.1:9999/delete/user/test
请求头：
Content-Type: application/json

Body：{"admin_user": "wintest", "token": "wintest1587830406"}
```
