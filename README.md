# AI Skill Analyzer

## 项目简介

这是一个基于 Python 和 FastAPI 的技能匹配分析系统。通过分析用户技能和岗位需求,计算技能匹配程度,并保存分析历史记录。

## 技术栈
Backend:
- Python 
- FastAPI 
- SQLAlchemy 
- MySQL 
- Pydantic 

## 项目结构

main.py
- FastAPI接口

analyzer.py
- 技能匹配核心逻辑

database.py
- 数据库连接和Session管理

models.py
- ORM模型

schemas.py
- 数据校验模型

sql/init.sql
- 数据库初始化脚本

## 环境与依赖

当前项目已验证使用 Python `3.14.2`。以下命令适用于 Windows PowerShell。

1. 进入后端项目目录，确认将用于创建环境的 Python 版本。项目放在其他位置时，请替换目录路径。

```powershell
cd D:\ai_analyzer
python --version
```

2. 首次使用、尚无 `.venv` 时，创建项目专用的虚拟环境。请先确认上一步显示的是准备使用的 Python 版本；已有可用 `.venv` 时跳过此步。

```powershell
python -m venv .venv
```

3. 使用项目虚拟环境安装依赖，避免安装到其他 Python 环境中。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

上述步骤是环境准备说明，尚未完成全新环境安装验证。日常启动时无需重复创建虚拟环境或安装依赖。

## 数据库连接配置

项目使用 MySQL。`database.py` 启动时先通过 `python-dotenv` 的 `load_dotenv()` 加载本地 `.env` 配置，再用 `os.getenv("DATABASE_URL")` 读取连接地址，不在源码中保存真实凭据。

MySQL 服务、数据库及表需先准备好。`sql/init.sql` 用于首次初始化，其中数据库名为 `ai_analyzer_db`，表名为 `analysis_history`；已有数据库时，不要为日常启动重复执行初始化脚本。

首次在本机使用时，在后端项目目录（与 `database.py` 同级）创建名为 `.env` 的文件，写入一行：

```dotenv
DATABASE_URL=mysql+pymysql://<用户名>:<密码>@<主机>:<端口>/<数据库名>
```

尖括号中的内容仅为占位说明，请在本机替换为有效连接信息，不能照抄为实际配置。真实账号密码只放本机 `.env`，不要写入源码、本说明或公开示例。文件内容使用 `名称=值` 格式，不写 PowerShell 的 `$env:` 前缀或 Python 语句。

`.env` 已加入 `.gitignore`，不随 Git 提交。换电脑或重新下载项目时，需另行创建这份本地配置；配置文件保留且地址有效时，后续新开终端启动无需重新输入连接地址，也不必重建虚拟环境或重装依赖。

默认情况下，终端中已存在的同名环境变量优先于 `.env`。若终端曾设置过旧地址，可在启动前清除该终端的临时值，让程序使用文件配置：

```powershell
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
```

若配置缺失或为空，程序会提示 `RuntimeError: DATABASE_URL环境变量未设置`。请检查本机 `.env` 的文件名、位置和配置内容，不要把真实地址改回源码。

## 运行方法

确认 MySQL 服务可用、数据库初始化已完成，且 `.venv` 依赖和本机 `.env` 均已准备好。在 Windows PowerShell 执行：

```powershell
cd D:\ai_analyzer
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

日常使用只需启动相关服务，无需每次手动设置 `DATABASE_URL`。保持后端终端运行；停止服务时按 `Ctrl+C`。

看到 `Application startup complete` 仅说明后端启动完成。再通过前端点击“加载历史”，或访问 `http://127.0.0.1:8000/history`，确认实际数据库查询正常。

用户已反馈：在新终端清除临时 `DATABASE_URL` 后，通过本机 `.env` 启动并查询历史正常。此前缺少配置时的明确报错也有运行证据，但发生于尚未引入自动读取文件的阶段；不将其冒充为当前版本移除全部配置后的重新测试。这些记录不等于已经完成全新环境安装与数据库初始化的完整复现。

## 接口示例

### POST /analyze

#### 请求示例

```json
{
  "position":"AI应用工程师",
  "user_skills":[
    "python",
    "react"
  ],
  "required_skills":[
    "python",
    "react",
    "vue"
  ]
}
```

#### 返回结果

```json
{
  "code":200,
  "message":"success",
  "data":{
    "matched":[
      "python",
      "react"
    ],
    "missing":[
      "vue"
    ],
    "rate":0.666
  }
}
```
## 当前进度

已完成：

- FastAPI连接MySQL
- SQLAlchemy ORM接入
- 分析记录保存
- 历史记录查询
- 数据库初始化脚本
- 统一响应格式
## JD技能提取练习（独立脚本）

`practice_llm.py` 使用 DeepSeek 官方 API，将脚本中的示例 JD 提取为技能列表，再调用已有 `analyzer.analyze` 规则计算技能匹配。它是有指导完成的学习练习，尚未接入网页、FastAPI 路由或数据库保存流程。

先按上文安装 `requirements.txt`，在本机 `.env` 中增加 `DEEPSEEK_API_KEY`；名称和空值示例见 `.env.example`。不要提交真实密钥。终端同名环境变量默认优先于文件配置。

在项目根目录运行：

```powershell
.\.venv\Scripts\python.exe .\practice_llm.py
```

每次运行都会向 DeepSeek 发送脚本中的 JD 并消耗已有 API 额度。模型名为 `deepseek-flash`，使用非思考模式；用户技能目前为脚本中的固定示例值。需要改变示例时先核对脚本，不把程序输出当作模型准确率统计。

已有验证：示例 JD 返回 Python、FastAPI、MySQL；用户技能 Python/MySQL 时，规则匹配率为 2/3；完整调用有本人运行结果。JSON格式错误、skills为字符串、百分比格式化分别做过本地验证。这里只验证对应样例，不表示完整鲁棒性。

当前限制：只检查 `skills` 是否为列表；未处理 JSON 顶层类型、缺失字段、列表非字符串元素和请求异常。脚本没有显式关闭客户端默认重试，勿将一次运行推定为网络失败时只尝试一次。模型字段或价格可能更新，调用前以[DeepSeek官方文档](https://api-docs.deepseek.com/zh-cn/)为准。
