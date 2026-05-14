<div align="center">
  <h1>
    <img src="./doc-image/logo.png" alt="EasyAccounts Logo" width="40" style="vertical-align: middle;" />
    EasyAccounts
  </h1>
  <p><strong>开源中文记账软件 · 数据自主可控 · AI 智能助手</strong></p>
  <p>
    <a href="https://github.com/QingHeYang/EasyAccounts/stargazers"><img src="https://img.shields.io/github/stars/QingHeYang/EasyAccounts?style=flat-square&logo=github" alt="Stars"></a>
    <a href="https://github.com/QingHeYang/EasyAccounts/network/members"><img src="https://img.shields.io/github/forks/QingHeYang/EasyAccounts?style=flat-square&logo=github" alt="Forks"></a>
    <a href="https://github.com/QingHeYang/EasyAccounts/blob/main/LICENSE"><img src="https://img.shields.io/github/license/QingHeYang/EasyAccounts?style=flat-square" alt="License"></a>
    <a href="https://hub.docker.com/r/775495797/easyaccounts-server"><img src="https://img.shields.io/docker/pulls/775495797/easyaccounts-server?style=flat-square&logo=docker" alt="Docker Pulls"></a>
    <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue?style=flat-square" alt="Platform">
  </p>
  <p>
    <a href="https://mercys-organization-2.gitbook.io/easyaccounts/">📚 文档</a> •
    <a href="./docs/deploy.md">🐳 部署</a> •
    <a href="./docs/feature-showcase.md">📸 截图</a> •
    <a href="./docs/changelog.md">📝 历史版本</a> •
    QQ群：817098590
  </p>
</div>

---

## 简介

EasyAccounts 是一款**开源中文记账软件**，支持本地 Docker 部署，数据完全自主可控。

新版本集成 **AI 智能助手**，可以通过对话查询、新增、修改流水，还能生成你想要的 Excel 报表。

如果你对互联网上的记账 App 不放心，担心**信息泄露**或**数据丢失**，也许这个项目能满足你的需求。

## 快速了解

| 项目 | 说明 |
|------|------|
| 👤 面向受众 | 个人 / 家庭 (不支持团队) |
| 🐳 部署要求 | 会使用 Docker Compose |
| 💻 支持平台 | Linux · Windows · macOS · 飞牛Fnos |
| 📦 资源消耗 | 内存 500-800MB |

## 核心特点

| 功能 | 说明 |
|------|------|
| 📝 记账管理 | 账户 · 收支操作 · 二级分类 · 明细流水 |
| 🔍 数据筛选 | 时间 · 账户 · 分类 · 备注 |
| 📊 报表生成 | 月度账单 · 筛选报表 · Excel 导出 · 自动月度 Excel |
| 🤖 AI 助手 | 对话记账 · 智能查询 · 图片识别 · MCP (SSE / Streamable-HTTP) |
| ⏰ 定时记账 | 周期账单自动生成（日 / 周 / 月 / 年）· 执行历史可查 |
| 📧 消息推送 | SQL 备份 · Excel 邮件推送 · 站内通知中心 |
| 🔐 安全特性 | 登录认证 · 单点登录 · 数据自主可控 |

## 项目部署

```bash
git clone https://github.com/QingHeYang/EasyAccounts.git
cd EasyAccounts
docker compose up -d
```

启动后访问 `http://你的IP:10669`

详细部署说明：[部署文档](./docs/deploy.md) | [GitBook](https://mercys-organization-2.gitbook.io/easyaccounts/)

## 版本动态

### v2.7.0

**重要特性**
- 新增 **定时记账**：周期性账单（订阅、房贷、水电、工资等）按规则自动生成流水，支持每日 / 每周 / 每月 / 每年，可暂停、修改、查执行历史
- 新增 **自动月度 Excel**：每月按时自动生成账单 Excel，可邮件发送，无需手动导出
- 新增 **站内通知中心**：双端顶栏铃铛 + 未读徽章，定时记账、Excel 生成等通知统一收口
- 新增 **统计页日支出折线图** + **明细页日合计**
- **设置全面 UI 化**：邮件 SMTP、备份时间、登录方式、自动 Excel 全部在前端「系统设置」配置，改完立即生效，**无需重启容器**
- AI 操作失败时前端会显示具体原因，不再静默卡住

**重要变更**
- ⚠️ WebHook 容器已废弃，邮件能力内置到 server。老用户升级请删除 `docker-compose.yml` 中 `webhook:` 服务块及 `SMTP_*` 等环境变量，在前端「系统设置 → 邮件」重新配置

完整说明：[v2.7.0 更新日志](./docs/changelog.md#270-2026-05)

### v2.6.2

- 新增 [OpenClaw Skills](https://github.com/QingHeYang/EasyAccounts-Skills) 集成（独立 Skill，无需升级容器）

### 下一版计划

> 我思路比较跳脱，很多情况下不会按照计划来

- 账单导入（目前可通过 [OpenClaw Skills](https://github.com/QingHeYang/EasyAccounts-Skills) 批量导入，原生入口规划中）
- 多账本
- 自定义筛选条件保存

查看完整版本历史：[更新日志](./docs/changelog.md) | [GitBook](https://mercys-organization-2.gitbook.io/easyaccounts/version)  
  

## 功能预览

<table>
  <tr>
    <td align="center">
      <img src="./doc-image/Feature-images/Mobile/board_all.png" width="180" />
      <br><b>总览</b>
    </td>
    <td align="center">
      <img src="./doc-image/Feature-images/Mobile/flow_all.png" width="180" />
      <br><b>明细</b>
    </td>
    <td align="center">
      <img src="./doc-image/Feature-images/Mobile/analysis_all.png" width="180" />
      <br><b>统计</b>
    </td>
    <td align="center">
      <img src="./doc-image/Feature-images/Mobile/ai_conversion.png" width="180" />
      <br><b>AI 对话</b>
    </td>
  </tr>
</table>

<table>
  <tr>
    <td align="center">
      <img src="./doc-image/Feature-images/Desktop/ai.png" width="280" />
      <br><b>AI 对话</b>
    </td>
    <td align="center">
      <img src="./doc-image/Feature-images/Desktop/analysis_all.png" width="280" />
      <br><b>统计分析</b>
    </td>
    <td align="center">
      <img src="./doc-image/Feature-images/Desktop/setting_type.png" width="280" />
      <br><b>分类设置</b>
    </td>
  </tr>
</table>

查看更多截图：[功能展示](./docs/feature-showcase.md)

## 功能说明

### 记账基础

记账围绕四个维度：**账户**、**收支操作**、**分类**、**明细**

- **账户**：你的钱放在哪，比如现金、银行卡、支付宝
- **收支操作**：钱怎么动的，收入、支出、借入、借出、内部转账（默认已配好，够用）
- **分类**：钱花在哪，支持二级分类，比如「用车」下面可以有「加油」「保险」
- **明细**：每一笔流水记录

记一笔账：选账户 → 选操作 → 选分类 → 填金额 → 保存，搞定。

### AI 助手

接入大模型 API，支持：
- 对话记账：「昨天午饭花了 25」
- 智能查询：「这个月花了多少」
- 图片识别：拍个小票自动识别
- MCP 功能：支持 SSE / Streamable-HTTP 协议

需要自己配置 API Key，支持多家大模型。

### 报表导出

两种 Excel 报表：
- **月度账单**：在明细页面生成当月账单
- **筛选账单**：按条件筛选后导出

> 小提示：生成历史月份账单时，账户余额会追溯到当时的金额

### 数据备份

- **SQL 自动备份**：在前端「系统设置 → 备份」配置备份时间，备份文件在 `Resource/sql/`
- **页面恢复数据**：直接在前端选择 SQL 备份文件即可恢复，无需手动映射
- **邮件推送**：在前端「系统设置 → 邮件」配置 SMTP，SQL 备份和 Excel 自动发到邮箱

<table>
  <tr>
    <td align="center">
      <img src="./doc-image/Email_get.png" width="280" />
      <br><b>邮件推送</b>
    </td>
    <td align="center">
      <img src="./doc-image/Email_sql.png" width="280" />
      <br><b>SQL 备份邮件</b>
    </td>
  </tr>
</table>

> v2.7.0 起，原 WebHook 容器已废弃，邮件能力内置到 server，所有配置改在前端 UI 完成，**改完立即生效，无需重启**。

### 开发者友好

- Swagger 接口文档：方便二次开发
- Nginx 文件服务：直接下载生成的文件

<table>
  <tr>
    <td align="center">
      <img src="./doc-image/Swagger_info.png" width="400" />
      <br><b>Swagger 接口文档</b>
    </td>
    <td align="center">
      <img src="./doc-image/Nginx_info.png" width="400" />
      <br><b>Nginx 文件下载</b>
    </td>
  </tr>
</table>

详见：[项目访问地址](https://mercys-organization-2.gitbook.io/easyaccounts/deploy/deploy#xiang-mu-fang-wen)

---

## 写在最后

这个项目从 2021 年 9 月开始，到现在已经 5 年多了。

我是个旧时代的 Android 工程师，从 2024 年开始大量用 AI 辅助开发（ChatGPT、Copilot、Cursor、Claude...），所以代码注释可能有点糙，请多包涵。

**重要提醒**：一定要保护好 SQL 备份数据，bug 可以修，项目可以重部署，但数据丢了就真没办法了。

这个项目会一直维护下去，因为我自己天天在用。有好点子随时告诉我，合适的话我会加上。

欢迎 Star，遇到问题欢迎提 Issue。项目永久免费开源。

另外我是个社恐，加微信、拉群这种事可能会有点迟疑，不是不想理你，是真的社恐，请多包涵。

**关于贡献**：目前新版本还在调试中，源码仓库暂时落后于发布版本，想参与贡献的朋友请耐心等待。

### 交流群

欢迎加入 QQ 群交流：817098590

<img src="./doc-image/QQ_Group.jpg" width="180" />

### 支持项目

如果你愿意支持 EasyAccounts，扫码捐赠的款项我会以 **EasyAccounts** 项目名义转赠至**腾讯公益孤儿救助项目**。

<table>
  <tr>
    <td align="center"><img src="./doc-image/WeChat.jpg" width="180" /></td>
    <td align="center"><img src="./doc-image/Ali_pay.jpg" width="180" /></td>
  </tr>
</table>

---

[![Star History Chart](https://api.star-history.com/svg?repos=QingHeYang/EasyAccounts&type=Date)](https://star-history.com/#QingHeYang/EasyAccounts&Date)