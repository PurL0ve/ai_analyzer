# AI Skill Analyzer

## 项目简介

基于Python和FastAPI的技能匹配分析系统，配合React前端使用。支持手动输入岗位要求，也支持从JD调用模型提取技能，再用规则计算匹配结果。当前仅手动分析流程保存历史，JD分析暂不保存。

## 技术栈
Backend:
- Python 
- FastAPI 
- SQLAlchemy 
- MySQL 
- Pydantic
- OpenAI兼容Python SDK与DeepSeek API

## 项目结构

main.py
- FastAPI接口

analyzer.py
- 技能匹配核心逻辑

jd_extractor.py
- JD模型请求、JSON解析与技能字段校验

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
    "rate":0.6666666666666666
  }
}
```
## JD技能提取与匹配

当前可复用实现是 `jd_extractor.py`。`extract_required_skills(jd)` 调用模型提取JD中的技能，`parse_required_skills(content)` 校验JSON及技能字段，再由 `analyzer.analyze` 完成规则匹配。DeepSeek模型负责提取，匹配率由规则计算。

### 模型配置

在后端本机 `.env` 中另行配置以下变量，保留已有 `DATABASE_URL`：

```dotenv
DEEPSEEK_API_KEY=<在本机填写有效密钥>
```

上面仅为占位说明，不是有效密钥；不要将真实值写入README或提交Git。当前代码使用 `openai` Python SDK连接 `https://api.deepseek.com`，模型为 `deepseek-flash`，使用非思考模式。服务可用性与额度需在使用时确认。

`jd_extractor.py` 在函数内初始化客户端，导入模块不会主动发送模型请求。当前 `__main__` 是本地JSON解析与规则匹配样例。旧 `practice_llm.py` 是历史练习，包含顶层真实请求，不作为日常启动入口，也不要为导入检查而运行或导入它。

### POST /analyze-jd

输入JD原文和本人技能，提取岗位要求后计算匹配结果。此接口不要求 `position` 或手填 `required_skills`，目前不保存数据库，也不会新增历史记录。

请求示例：

```json
{
  "jd": "招聘Python后端开发工程师，要求掌握Python、FastAPI和MySQL。",
  "user_skills": ["Python", "MySQL"]
}
```

2026-10-22本人通过接口文档执行该样例，实际HTTP状态为200，返回：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "matched": ["python", "mysql"],
    "missing": ["fastapi"],
    "rate": 0.6666666666666666
  }
}
```

这是该样例的实际结果，不保证模型对所有JD都返回同样顺序或正确技能。最终匹配结果不是模型原始回复；原始回复未单独留存。匹配率表示当前技能集合规则下的匹配程度，不是录用概率。

空白JD在请求模型前返回HTTP400：

```json
{"detail": "JD不能为空"}
```

提取函数返回 `None` 时，接口实现为HTTP502、`detail` 为 `JD技能提取失败`；此分支尚未在新接口上运行验证，提示暂不区分超时和无效回复。缺少请求字段或字段类型不符合Pydantic模型时，由FastAPI进行请求校验；不要把接口文档的示例响应当作已经实测。

非空JD请求会调用外部模型并使用API额度。客户端未显式设置超时值或关闭SDK默认重试，一次界面操作不保证只有一次底层网络尝试。不要连续点击或用反复请求证明同一结果。

### GET /history

查询现有 `analysis_history` 记录，通过 `ResponseModel` 返回列表。当前没有分页或显式排序。旧 `POST /analyze` 仍进行手动技能匹配并保存数据库；JD分析尚未加入这条保存流程。

## 当前功能与验证范围

截至2026-10-22，已实现：

- 手动技能输入、清洗去重、规则匹配与统一成功响应。
- SQLAlchemy/MySQL分析记录保存、提交失败回滚和历史查询。
- JD真实模型提取、JSON顶层对象检查、`skills`列表及字符串元素检查。
- `POST /analyze-jd` 与React“从JD分析”入口。
- 模型请求的 `APITimeoutError` 捕获、提示并返回 `None`。

已有本人运行证据：

- JD解析相关本地样例，以及顶层列表/非字符串元素的拦截与正常匹配；不同改动后的验证范围分别记录，未完成一次覆盖所有边界的完整回归。
- 新接口空白JD的实际HTTP400，以及正常JD的真实请求HTTP200。
- React输入JD后显示Python/MySQL匹配、FastAPI缺失、66.7%；有等待与成功恢复截图，以及前端空输入和请求失败提示截图。
- 前端本人生产构建通过。

这些是有指导实现和本人操作证据，不代表全程独立开发、整体准确率或所有异常路径通过。内置 `TimeoutError` 的本地模拟已运行；真实SDK超时捕获目前只有静态检查，不能用前者替代后者的实测。

## 已知限制与待完善

- JD分析结果尚不保存历史；手动分析的历史流程继续保留。
- SDK真实超时、其他连接/HTTP错误及新接口502等尚未全面验证或处理。
- 尚未形成一组固定JD样例的提取效果评估；用户仍需核对模型提取。
- 尚未完成全新环境按说明安装、初始化并运行的完整复现。
- 当前是本地演示项目；尚无公开部署验收或多用户认证/数据隔离验收。
- 未实现RAG、Agent或个人能力档案，后续依据实际需求安排。
