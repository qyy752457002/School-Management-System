# 项目更新说明

## 1. 包管理

### 1.1 确保安装如下包
```bash
pip install --upgrade pip

pip install "psycopg[binary,pool]"

pip install id-validator

pip install xlsxwriter

```

### 1.2 更新包

在项目目录下执行如下命令

```bash
# Windows
 pip install -r .\requirements.txt
```

```bash
# linux/unix/macos
 pip install -r ./requirements.txt
```

### 1.3 数据库升级

在项目目录下执行如下命令

python main.py db-init revision

python main.py db-init upgrade

todo  状态键编辑接口


## 2. Example Code

### 2.1 分页的示例

`/api/school/v1/planningschool/page`

## 3.数据库合并
alembic merge -m "Merge heads" b16e943b436d f93abb78988a
cfe1085d4785, ee0318e103ba





2.分校的用 学校的 组织   
分校更新后  更新 学校的组织包含的 分校数据 (服务范围)


就是单位加入组织(即 新增  修改服务范围)
分校同时隶属自己的组织  和 学校的组织  多组织

3.部门隶属单位  就是部门隶属学校  发送过去  
部门要加编号  学校内唯一 不能重复  用于在发送人时把 编号发送过去 


4.todo 年级 添加  届别 都加部门

5.家长属于多个部门 ? (即多个子女在不同的学校或者不同的班级)







