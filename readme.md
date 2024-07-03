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


