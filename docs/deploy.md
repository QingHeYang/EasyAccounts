# EasyAccounts 部署文档

## 重要声明

> **版本说明**：从 2.6.0 版本开始，各容器采用独立版本号管理，不再统一使用 `latest` 标签。
>
> | 容器 | 当前版本 |
> |------|----------|
> | easyaccounts-mysql | 2.7.0 |
> | easyaccounts-nginx | 4.1.0 |
> | easyaccounts-server | 2.7.0 |
> | easyaccounts-ai | 1.2.0 |
> | ~~easyaccounts-webhook~~ | **v2.7.0 起已废弃**（邮件功能并入 server） |

> **v2.7.0 重要变更**：
> - WebHook 容器已废弃，邮件发送由 server 内置
> - 备份时间、登录配置、SMTP 等不再通过环境变量配置，改在前端「**系统设置**」UI 中配置
> - 老用户升级请参考 [v2.7.0 升级说明](./changelog.md#270-2026-05)

> **关于国内镜像**：`docker-compose-chinese.yml` 已停止支持与更新，因阿里云停止了免费的镜像仓库服务，无法继续上传镜像。

> **旧版本**：如果不想使用最新版本，可以切换到对应分支：
> ```bash
> git checkout 2.6.1   # 切到 v2.6.x（仍使用 webhook 容器与环境变量配置）
> git checkout 2.5.0   # 切到 v2.5.0
> ```

---

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/QingHeYang/EasyAccounts.git

# 2. 进入目录
cd EasyAccounts

# 3. 启动服务
docker compose up -d
```

首次启动需要拉取镜像，请耐心等待。启动成功后访问 `http://你的IP:10669` 即可使用。

---

## 容器说明

项目包含 **4 个容器**（v2.7.0 起 webhook 已废弃），通过 Docker 内部网桥 `easy_accounts_net` 互相通信。

### 1. db (MySQL 数据库)

**镜像**：`775495797/easyaccounts-mysql:2.7.0`

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| TZ | 时区 | Asia/Shanghai |
| MYSQL_ROOT_PASSWORD | 数据库 root 密码 | easy_accounts |
| MYSQL_DATABASE | 数据库名称（勿改） | yd_jz |

**数据目录**：`./Database/data`

**注意**：请勿修改服务名 `db`，否则后端无法连接数据库。

**恢复数据库**：

如需从备份恢复数据库，按以下步骤操作：

```bash
# 1. 创建初始化目录
mkdir -p Database/init

# 2. 将备份文件放入初始化目录（文件名格式：yd_jz_{yyyyMMdd_HHmm}.sql）
cp Resource/sql/yd_jz_20250101_1200.sql Database/init/

# 3. 解开 docker-compose.yml 中的初始化映射注释
# - ./Database/init:/docker-entrypoint-initdb.d

# 4. 删除旧数据
rm -rf Database/data/*

# 5. 重启服务
docker compose down
docker compose up -d
```

---

### 2. nginx (前端服务)

**镜像**：`775495797/easyaccounts-nginx:4.1.0`

**端口**：`10669:80`（唯一对外暴露的端口）

**数据目录**：
- `./Resource` → 资源文件下载目录

---

### 3. server (后端服务)

**镜像**：`775495797/easyaccounts-server:2.7.0`

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| DB_PASSWORD | 数据库密码 | easy_accounts |

**可选配置**（外部数据库）：
| 环境变量 | 说明 |
|----------|------|
| MYSQL_HOST | 数据库地址 |
| MYSQL_PORT | 数据库端口 |
| MYSQL_USERNAME | 数据库用户名 |

> **v2.7.0 配置迁移**：以下环境变量已从容器配置下沉到前端「**系统设置**」UI，启动后在 Web 端配置，**改完立即生效，无需重启容器**：
>
> | 旧环境变量 | 迁移到 |
> |-----------|--------|
> | `SQL_BACKUP_TIME` | 系统设置 → 备份 |
> | `ENABLE_LOGIN` | 系统设置 → 鉴权 |
> | `EXPIRED_TIME` | 系统设置 → 鉴权 |
> | `SINGLE_LOGIN` | 系统设置 → 鉴权 |
> | webhook 容器 `SMTP_*` | 系统设置 → 邮件 |

**数据目录**：
- `./Resource/sql` → SQL 备份文件
- `./Resource/excel/month` → 月度账单
- `./Resource/excel/screen` → 筛选账单
- `./Resource/images` → 上传的图片
- `./Server/logs` → 日志文件
- `./Server/auth` → 登录认证文件（删除 `secret.key` 可重置密码）

---

### 4. ai (AI 智能助手，可选)

**镜像**：`775495797/easyaccounts-ai:1.2.0`

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| LLM_EASY_ACCOUNTS_API_KEY | LLM API Key | - |
| LLM_EASY_ACCOUNTS_URL | LLM API 地址 | https://api.openai.com/v1 |
| LLM_EASY_ACCOUNTS_MODEL | 使用的模型 | gpt-3.5-turbo |
| MCP_SERVER_ENABLED | 是否启用 MCP 服务器 | false |
| MCP_TRANSPORT_MODE | MCP 传输模式 | sse |

**MCP 传输模式**：
- `sse`：Server-Sent Events
- `streamable-http`：Streamable HTTP

**数据目录**：
- `./AI/database` → AI 数据库
- `./AI/logs` → AI 日志
- `./AI/小易.role` → 自定义 AI 角色
- `./AI/task.prompt` → 自定义 AI 指令

如不需要 AI 功能，可在 `docker-compose.yml` 中删除或注释整个 `ai` 服务块。

---

## 常用命令

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 查看日志
docker logs easy_accounts_server -f
docker logs easy_accounts_ai -f

# 更新镜像
./update-docker.sh

# 重启单个服务
docker compose restart server
```

---

## 邮件配置（v2.7.0 起）

SMTP 配置入口已迁移到前端：

1. 启动后访问前端，进入「**系统设置 → 邮件**」
2. 填写 SMTP 服务器、端口、发件邮箱、授权码、收件人等信息
3. 保存即可，无需重启容器

老用户从 v2.6.x 升级时，原 `docker-compose.yml` 中的 `webhook:` 服务块和 `SMTP_*` 环境变量需删除，配置在 UI 中重新填写。

---

## 更多信息

- [详细部署教程](https://mercys-organization-2.gitbook.io/easyaccounts/deploy/deploy)
- [v2.7.0 升级说明](./changelog.md#270-2026-05)
