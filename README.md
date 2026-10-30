# 电商售后机器人

基于 FastAPI + SQLAlchemy + SQLite 的电商售后智能客服系统：自动识别用户售后诉求，创建工单并持久化到数据库，同时提供工单查询与状态流转接口。

## 功能清单

| 模块 | 说明 |
| --- | --- |
| 意图识别 | 命中「退款/退货/换货/售后/维修/坏了/破损/漏发/少发」即创建工单 |
| 工单创建 | `POST /api/chat` 自动建单并返回 `ticket_id` |
| 工单查询 | 按用户查询全部工单、按 ID 查询单个工单 |
| 状态流转 | `pending → processing → resolved → closed` |
| 接口文档 | 启动后访问 `/docs` 在线调试 |
| 自动化测试 | pytest + TestClient，覆盖正常咨询、建单、查询、改状态、异常 |

## 技术栈

Python 3.10 · FastAPI 0.110.0 · SQLAlchemy 2.0.28 · Pydantic 2.6.4 · Uvicorn · SQLite

## 快速开始

```powershell
# 1. 进入项目
cd D:\projects\ecommerce-after-sales-bot

# 2. 创建并激活虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 3. 安装依赖
python -m pip install -r requirements.txt

# 4. 启动（--reload 支持代码热更新）
python -m uvicorn main:app --reload
```

启动成功后访问：http://127.0.0.1:8000/docs

## 接口速览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/chat` | 咨询或创建售后工单 |
| GET | `/api/tickets?user_id=` | 查询用户全部工单 |
| GET | `/api/tickets/{id}` | 查询单个工单 |
| PATCH | `/api/tickets/{id}` | 更新工单状态 |

### 测试示例

```bash
# 创建售后工单
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test_001","message":"我要退款"}'

# 查询工单
curl http://127.0.0.1:8000/api/tickets?user_id=test_001
```

## 运行测试

```powershell
python -m pip install pytest pytest-asyncio httpx
python -m pytest tests -v
```

## 项目结构

```
ecommerce-after-sales-bot/
├── main.py               # 应用入口，启动时建表
├── db.py                 # 数据库配置与 Ticket 模型
├── api/
│   ├── main.py           # 接口实现与意图识别
│   └── schemas.py        # 请求/响应数据模型
├── tests/
│   └── test_api.py       # 自动化测试
├── requirements.txt
├── Dockerfile
└── .gitignore
```

## 后续扩展方向

- 接入大模型（扣子/OpenAI 兼容接口）实现多轮对话与更精准的意图分类
- 对接《电商售后》知识库，按规则作答并标注适用条件
- 增加管理员视角：工单池、分配客服、超时提醒
- 增加日志表与统计接口（今日工单数、平均处理时长）
