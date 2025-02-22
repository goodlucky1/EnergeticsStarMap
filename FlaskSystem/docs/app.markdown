```markdown
# 接口文档

## 概述
本文档提供系统API的详细说明，涵盖用户认证、文件管理、数据操作三大模块。所有接口均基于Flask框架实现，数据存储于MySQL数据库。

## 认证与授权
- 使用Cookie进行身份验证，登录/注册后返回`token`和`username`的Cookie
- 用户角色权限等级：
  - 管理员：100
  - 教师：10 
  - 学生：1

---

## 认证模块（/auth）

### 1. 用户登录
**URL**  
`POST /auth/login`

**请求参数**  
```json
{
  "username": "string",
  "password": "string"
}
```

**响应示例**  
成功：
```json
{
  "code": 200,
  "message": "Login successful"
}
```
失败：
```json
{
  "code": 401,
  "message": "Login fail"
}
```

**Cookie**  
- token: 用户权限等级
- username: 用户名
- 有效期：1天

---

### 2. 用户注册
**URL**  
`POST /auth/register`

**请求参数**  
```json
{
  "username": "string",
  "password": "string"
}
```

**响应示例**  
成功：
```json
{
  "code": 200,
  "message": "Register successful"
}
```
用户名已存在：
```json
{
  "code": 401,
  "message": "Username already exists"
}
```

**Cookie**  
同登录接口

---

### 3. 修改用户信息
**URL**  
`GET /auth/revise`

**请求参数**  
```json
{
  "username": "string",
  "password": "string（可选）",
  "usertype": "string（可选）"
}
```

**响应示例**  
成功：
```json
{
  "code": 200,
  "message": "revise successful"
}
```

---

## 文件模块（/file）

### 1. 文件上传
**URL**  
`POST /file/upload`

**请求格式**  
`multipart/form-data`

**参数**  
- files: 文件对象

**响应示例**  
```json
{
  "code": 200,
  "msg": "上传成功,文件已经保存于服务器"
}
```

---

### 2. 文件列表
**URL**  
`GET /file/list`

**响应示例**  
```json
{
  "code": 200,
  "msg": "文件列表",
  "files": {
    "filename1": 1024,
    "filename2": 2048
  }
}
```

---

### 3. 文件下载
**URL**  
`POST /file/download`

**请求参数**  
```json
{
  "filename": "string"
}
```

**响应**  
返回文件内容（二进制流）

---

## 数据模块（/data）

### 通用说明
- 所有接口需要携带`token`和`username` Cookie
- 权限要求：
  - 添加数据：权限等级 ≥ 10（教师及以上）
  - 修改/删除数据：权限等级 ≥ 10
  - 获取数据：管理员/教师可查看全部，学生仅限自身

---

### 1. 批量导入数据
**URL**  
`POST /data/import`

**请求参数**  
```json
{
  "studata": [{...}, {...}],
  "teachername": "string"
}
```

**响应示例**  
```json
{
  "code": 200,
  "msg": "数据导入成功"
}
```

---

### 2. 添加单条数据
**URL**  
`POST /data/add`

**请求参数**  
```json
{
  "studata": {...},
  "teachername": "string"
}
```

---

### 3. 数据查询
**URL**  
`POST /data/getdata`

**学生请求**  
```json
{
  "studentname": "string"
}
```

**教师请求**  
```json
{
  "teachername": "string"
}
```

**响应示例**  
```json
{
  "code": 200,
  "msg": "数据获取成功",
  "data": [...]
}
```

---

## 数据库配置
```python
DB_CONFIG = {
    'host': '10.10.116.210',
    'port': 3306,
    'user': 'root',
    'password': 'Password123$',
    'db': 'db'
}
```

## 错误代码表
| 代码      | 说明        |
|---------|-----------|
| 200     | 成功        |
| 201     | 不确定是否成功   |
| 401/402 | 认证失败/数据冲突 |
| 403     | 权限不足      |
| 404     | 资源不存在     |
```