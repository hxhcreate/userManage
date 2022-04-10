> 练习Python 后端的初步项目 主要聚焦用户管理
>
> 将尝试不同的数据库 不同的数据库驱动
>

### 部分疑难问题

- token问题

 ```
 记录当前用户只要在线  则可以以该用户的角色信息来进行操作
 用于用户的快速登录
 ```

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


提示：sex可以没有  不提供role注册接口
```

- 用户登录接口请求示例：

```
请求方式：POST
请求地址：http://127.0.0.1:9999/login
请求头：
Content-Type: application/json

Body：{
    "username": "wintest",
    "password": "123456"
}
```

- 管理员修改用户接口请求示例（ token 可以从用户登录成功后的接口返回数据中获取）：

```
请求方式：PUT
请求地址：http://127.0.0.1:9999/users/admin/update/4
请求头：
Content-Type: application/json

Body：{"admin_user": "wintest", "token": "f54f9d6ebba2c75d45ba00a8832cb593", "sex": "1", "address": "广州市天河区", "password": "12345678", "telephone": "13500010003"}
提示：操作用户 token 新用户名 电话 密码必须都提供
```

- 修改自身用户接口请求示例（ token 可以从用户登录成功后的接口返回数据中获取）：

```
请求方式：PUT
请求地址：http://127.0.0.1:9999/users/update/:username
请求头：
Content-Type: application/json

{"token": "8ff5ec53610e97743ffa97e8df58365c" , "username": "wintest", "password": "123456", "sex": "1", "telephone":"18500010005", "address": "上海市黄浦区"}
提示： token 新用户名 新电话 新密码必须都提供
```

- 管理员删除用户接口请求示例（ token 可以从用户登录成功后的接口返回数据中获取）：：

```
请求方式：DELETE
请求地址：http://127.0.0.1:9999/users/admin/delete/wintest
请求头：
Content-Type: application/json

Body：{"admin_user": "root", "token": "wintest1587830406"}
```
