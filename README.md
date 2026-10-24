# AI Skill Analyzer

## 项目简介

基于Python和FastAPI的技能匹配分析系统，配合React前端使用。支持手动输入岗位要求，也支持从JD调用模型提取技能，再用规则计算匹配结果。手动分析和JD分析均将匹配记录保存到同一张历史表，前端可手动加载查看；JD原文暂不保存。

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
- 历史记录响应与统一响应模型；请求模型定义在main.py中

sql/init.sql
- 数据库初始化脚本

### 辅助脚本与学习练习

以下文件不参与正常网页请求链路，不因放在后端目录就成为业务入口：

- `evaluate_jd_prompt.py`：离线提示词评估与技能差集对照工具。当前直接运行的入口使用已保存的列表，比较后写入、读回 `jd_comparison.json`；真实模型调用示例保持注释。文件中的 `evaluate_prompt` 只有被主动调用才请求模型；主入口保护避免导入时自动执行底部比较和文件读写。
- `check_jd_failure.py`：使用临时替换和TestClient验证提取失败分支，不是后端启动入口。当前JD请求新增必填 `position`，旧验证脚本若仍缺该字段，需要先核对更新，不能直接沿用旧回执。
- `practice_save_failure.py`：手动分析保存失败的模拟练习，不替代JD接口本轮保存失败的证据。
- `test_db.py`：数据库增改删验证脚本，含真实提交操作，不作为普通查询或日常启动入口。
- `practice_json_count.py`、`practice_transaction.py`、`practice_llm.py`：历史学习练习。事务练习使用内存SQLite；旧LLM练习含顶层真实请求，不运行或导入它来做普通检查。

正常业务请求从 `main.py` 进入，调用 `analyzer.py`、`jd_extractor.py` 及数据库相关模块；不需要运行上述练习才能使用网页。

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

当前建表定义包含 `source VARCHAR(20) NULL DEFAULT NULL`。升级旧数据库时，先查看 `SHOW COLUMNS FROM ai_analyzer_db.analysis_history;`；仅在确认缺少source列后，单独执行以下迁移，不要重复执行，也不要重新建表：

```sql
ALTER TABLE ai_analyzer_db.analysis_history
ADD COLUMN source VARCHAR(20) NULL DEFAULT NULL;
```

修改 `models.py` 或保存 `init.sql` 不会自动修改已有表。上述语句保留旧行，旧记录来源保持NULL；不批量回填为manual。本机已完成此字段迁移及结构核对；尚未在全新环境重新初始化验证。

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

输入岗位名称、JD原文和本人技能，提取岗位要求后计算匹配结果，并提交一条 `analysis_history` 记录。`position`、`jd`、`user_skills` 均为请求字段，不需要手填 `required_skills`。

请求示例（当前请求结构）：

```json
{
  "position": "Python后端实习生",
  "jd": "招聘Python后端开发实习生，要求掌握Python、FastAPI和MySQL。",
  "user_skills": ["Python", "MySQL"]
}
```

成功响应结构示例：

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

示例用于说明当前契约，不表示对上面的新请求重新调用过模型。2026-10-22旧版JD接口已有真实HTTP200和上述66.7%匹配结果，但当时尚无本次必填岗位名称及保存流程；不能把旧结果当作当前版本完整链路的重新验收。模型结果与顺序可能波动，最终匹配结果也不是模型原始回复。匹配率是名称规则下的技能匹配程度，不是岗位胜任度或录用概率。

保存内容为岗位名称、用户技能、提取出的岗位技能、匹配率和创建时间；技能列表沿用现有英文逗号连接格式。手动分析和JD分析共用历史表，来源由后端接口确定：新手动记录为 `source="manual"`，新JD记录为 `source="jd"`；新增字段前的旧记录保留 `NULL`，不推断其来源。仍不保存JD原文。成功响应在 `db.commit()` 完成后返回。

输入与失败处理：

- 空白 `jd`：在提取前返回HTTP400，正文如下。

```json
{"detail": "JD不能为空"}
```

- 空白 `position`：在提取前返回HTTP400，正文如下。

```json
{"detail": "岗位名称不能为空"}
```

- 提取函数返回 `None`：返回HTTP502及 `JD技能提取失败`。提示暂不区分超时和无效回复；2026-10-23旧版接口已有临时替换为None的隔离验证；2026-10-24补充本地实际SDK超时被业务函数捕获并返回None的验证。两者为不同运行，实际SDK超时经过接口返回502的同次联合路径及运行中服务器/网页真实502仍未验收。
- 添加或提交记录时捕获 `SQLAlchemyError`：调用 `db.rollback()`，返回HTTP500及 `数据库保存失败`。本轮仅用Mock提交异常验证回滚方法被调用及500响应，未制造真实数据库故障。
- 缺少请求字段或类型不符合请求模型：由FastAPI进行请求校验。不要把说明或接口示例当作已经完成全部边界验证。

2026-10-24本人使用TestClient，在提取被固定为Python/FastAPI的条件下，实际得到HTTP200及匹配Python、缺失FastAPI、rate为0.5；随后通过 `/history` 查回数据库记录，并在网页看到对应岗位及50.0%。它验证固定提取结果下的保存、查询与展示，不是浏览器真实模型调用到保存的整条新链路验收。

输入通过校验后，正常调用该接口会请求外部模型并使用API额度；成功时还会新增历史记录，不要反复调用同一个样例。业务提取客户端现显式设置 `timeout=30`、`max_retries=0`：网络操作等待超时为30秒，失败后不自动重试。该设置不保证整个接口严格在30秒内结束；目前作为初始配置，尚未验证其是否适合正常的外部模型请求。此配置位于 `jd_extractor.py`，不自动改变离线评估脚本的客户端配置。


### 超时验证范围与当前配置

2026-10-24晚间补充三类有指导、本人操作证据，不能混为同一次测试：

- 模拟异常：将模拟客户端的create设为抛出 `APITimeoutError`，运行原提取函数，实际打印超时提示并返回None；证明捕获分支可处理该异常对象，不证明网络真的超时。
- 实际SDK连接超时：真实SDK请求本机8765端口，占位密钥、2秒等待、零重试、禁用环境代理，外层捕获输出 `APITimeoutError` 及直接原因 `ConnectTimeout`；没有人为抛异常，不把连接超时写成读取响应超时。
- 实际SDK超时经过业务函数：真实SDK请求本机8766端口，通过临时替换业务客户端构造、dotenv和getenv，使原提取函数使用该本地客户端；create方法没有被Mock或人为raise，实际打印“请求超时，请稍后再试”并返回None。该轮未打印底层原因类型，不认定为ReadTimeout，也不沿用上一轮ConnectTimeout。

本地测试未请求DeepSeek、未使用真实密钥、未写数据库；临时替换退出后恢复，客户端、连接与监听端均已由本人反馈关闭。未计时，不声称精确2秒。没有经过HTTP接口，不把以上与旧None→502隔离验证拼成一次联合实测。

上述运行使用测试客户端2秒/零重试配置。之后本人在 `jd_extractor.py` 将业务参数设为30秒/零重试，仅做静态核对，原提取、捕获及解析流程保留；未追加外部模型请求。正式等待阈值尚需按实际使用评估，不能从本地测试推出最优参数。

### GET /history

查询现有 `analysis_history` 记录，通过 `ResponseModel` 返回列表，包含已成功保存的手动分析和JD分析记录。历史响应包含可空的 `source` 字段；前端将 `manual` 显示为“手动输入分析”、`jd` 显示为“JD提取分析”，其他值显示“历史未标记”。当前没有分页或显式排序；页面展示编号是列表序号，不是数据库主键。前端需点击“加载历史”刷新列表，新记录不会自动出现。

## 当前功能与验证范围

截至2026-10-24，已实现：

- 手动技能输入、清洗去重、名称规则匹配和统一成功响应。
- JD模型提取、JSON顶层对象检查、`skills`列表及字符串元素校验。
- `POST /analyze-jd`接收岗位名称，空白岗位名称/JD在提取前拦截；成功匹配记录保存到现有历史表。
- 手动分析与JD分析的数据库保存、提交异常回滚调用及历史查询代码；新增记录保存manual/jd来源，历史响应允许旧记录source为空。
- React“从JD分析”入口、岗位名称空输入提示，以及后端非空文字detail/通用文案两类错误提示。
- 模型请求捕获 `APITimeoutError`、提示并返回 `None`；本地受控端点下实际SDK超时经过业务捕获已有本人运行证据，外部DeepSeek超时未测。业务客户端显式设置30秒网络操作超时、关闭自动重试。

已有本人运行与页面证据：

- 2026-10-24当前版本网页样例 `JD真实闭环验证_20261024_01`：匹配python/mysql、缺少fastapi、66.7%；网络响应正文code为200、message为success，历史出现同名记录及66.7%。此组截图未展示Headers中的HTTP状态，不把正文code当作HTTP状态实测；这是本次真实网页成功样例，区别于此前固定提取验证。
- 实际数据库已新增允许NULL的 `source VARCHAR(20)`；`models.py`、历史响应和 `sql/init.sql` 定义已同步。旧历史响应source为null，页面显示“历史未标记”；新手动样例历史响应source为manual、rate为0.5，页面显示对应来源；新JD样例临时固定提取Python/FastAPI后返回HTTP200、rate为0.5，网页显示JD来源。临时替换已停止，此JD来源样例不验证真实模型提取效果。

- 历史JD解析正反样例、旧版空白JD HTTP400、旧版真实JD HTTP200及网页66.7%结果；不同版本的证据分开，不当作一次完整回归。
- 2026-10-24前端空岗位名称提示；当前后端在有效JD、空格岗位名称下的TestClient HTTP400及“岗位名称不能为空”。
- 固定提取Python/FastAPI后，JD接口实际保存记录；`/history`查回记录并在网页显示50.0%。
- 模拟JD提交异常时返回HTTP500及“数据库保存失败”，Mock回滚方法调用1次；不证明真实故障后的数据库事务状态。
- 前端临时模拟HTTP502：非空文字detail显示具体提示，缺少detail时显示通用提示；不是实际服务器502或SDK超时。
- 来源展示版本人生产构建通过：Vite8.3.1、18模块、198ms，JS产物index-B2nW8GaZ.js。之后仅调整两处中文来源名称，已有更新后的页面截图，未另提供构建回执。本机单次构建时长不外推性能，也不替代部署、lint或全环境复现。
- 离线评估已保留一条完整产品经理JD的两版真实提取输出，以及一个信息不足样本的空技能输出；有人工参考、差集和JSON保存/读回练习。原始第一次仅岗位名的错误输入不纳入完整JD对照。修改稿并无明确更好证据，业务提示词未替换。

以上为有指导实现与本人操作证据，不代表全程独立开发或独立迁移。模拟数据、Mock及临时fetch替换均与真实模型、真实数据库故障区分；不根据少量样本声称整体准确率。

## 已知限制与待完善

- JD与手动分析共用历史表，已有来源标记；旧记录保留未知来源，不保存JD原文，也无分页或显式排序。
- 当前版本已有一次“浏览器→真实模型提取→数据库保存→历史展示”成功样例；该样例不替代完整回归、独立实现或全部异常路径验收。来源字段另用手动分析与固定提取JD样例验证，未为来源标记再次调用真实模型。
- 本地实际SDK超时转换与业务捕获已有验证；外部DeepSeek服务超时、实际SDK超时到HTTP502的同次联合路径、其他连接/HTTP错误及完整边界回归仍未全面验证或处理。30秒/零重试配置仅静态核对，未据此重跑外部请求或验证整体接口耗时上限。
- JSON结构合格不等于提取正确。匹配仅按清洗后的名称相等，不进行同义词/语义匹配，不区分必备与优先；空提取列表的rate为0，不代表用户确实一个技能都不匹配。
- 评估仍是小样本准备与有指导验证，未证明提示词稳定改善，也未形成整体效果、调用成本或准确率结论。
- 尚未完成全新环境安装、初始化和运行的完整复现，以及公开部署或多用户认证/数据隔离验收。
- 未实现RAG、Agent或个人能力档案，后续依据实际需求安排。
