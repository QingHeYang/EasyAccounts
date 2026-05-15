---
icon: rocket
description: EasyAccounts 部署相关文档
---

# 部署

本章节介绍 EasyAccounts 的 Docker 部署、AI 助手配置等内容。

## 子章节

- [EasyAccounts 项目部署](deploy.md) — 详细的 Docker 部署教程
- [AI 智能助手部署](ai.md) — 配置内置 AI 服务（可选）
- [OpenClaw Skill](openclaw-skill.md) — 通过 OpenClaw / Claude Skill 协议接入外部 AI 助手
- [WebHook 功能介绍](webhook.md) — ⚠️ v2.7.0 起已废弃，仅供老用户参考

## 快速开始

```bash
git clone https://github.com/QingHeYang/EasyAccounts.git
cd EasyAccounts
docker compose up -d
```

启动后访问 `http://你的IP:10669` 即可使用。

不同平台的特殊部署方式请参见 [多平台部署](../platform/README.md)。
