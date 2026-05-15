---
icon: hand-pointer
description: 在 OpenClaw / Claude Skill 协议中接入 EasyAccounts
---

# OpenClaw Skill

通过 [OpenClaw](https://github.com/QingHeYang/EasyAccounts-Skills) Skill 协议把 EasyAccounts 接入 AI 助手（OpenClaw / Claude Desktop 等），用自然语言记账、查账、做统计。

> 项目地址：[https://github.com/QingHeYang/EasyAccounts-Skills](https://github.com/QingHeYang/EasyAccounts-Skills)

## 能做什么

- **记一笔流水**：「记一下午餐 30 块」
- **批量记账**：「今天的：午餐 30、地铁 12、咖啡 25」
- **查询流水**：「查上个月的餐饮支出」、「今年最大的 5 笔开销」
- **修改流水**：「把刚才那笔午餐改成 35」
- **内部转账**：「从微信转 500 到银行卡」
- **年度统计**：「今年总收入多少」、「现在总资产多少」
- **导出 Excel**：「把 3 月的账单导出」
- **系统信息**：「有什么新公告」、「我用的什么版本」

{% hint style="info" %}
所有通过 Skill 创建的流水会标记 `from=Claw`，备注末尾追加 `#Claw记账`，方便你溯源。
{% endhint %}

## 安装

```bash
clawhub install easyaccounts
# 或
openclaw skills install easyaccounts
```

## 配置

在 `~/.openclaw/.env` 中设置：

```bash
# 必需
EASYACCOUNTS_URL=http://your-easyaccounts-server:8081
# 或带 nginx 代理路径
# EASYACCOUNTS_URL=http://example.com/api

# 可选（仅服务端开启了登录时需要）
EASYACCOUNTS_USERNAME=admin
EASYACCOUNTS_PASSWORD=yourpassword
```

{% hint style="warning" %}
**安全建议**：`chmod 600 ~/.openclaw/.env` 限制权限，避免凭据泄露。
{% endhint %}

## 依赖

- `curl`（几乎所有系统自带）
- `jq` — JSON 处理
  - macOS：`brew install jq`
  - Ubuntu/Debian/WSL：`apt install jq`
  - Windows：推荐 WSL2，或下载 [jq for Windows](https://jqlang.github.io/jq/download/)

OpenClaw 在 Windows 推荐使用 WSL2，本 skill 在 WSL2 内运行无需额外配置。

## 使用示例

> **你**：今天午餐花了 35，记一下
> **AI**：已记录，流水 #4828：现金 -35.00，分类：餐饮，日期：2026-04-07

> **你**：查一下这个月吃饭花了多少
> **AI**：本月餐饮支出共 8 笔，合计 ¥523.50，占总支出 31%。最大一笔是…

> **你**：今天的：午餐 30、地铁 12、咖啡 25，记一下
> **AI**：已批量记 3 笔，总计 ¥67.00 …

## 不支持的操作

{% hint style="danger" %}
出于**安全考虑**，本 Skill **不提供以下功能**：

- ❌ 删除流水（需到 EasyAccounts 前端手动删除）
- ❌ 删除账户 / 分类
- ❌ 修改账户余额
- ❌ 任何破坏性 / 不可逆操作

如需上述操作，请通过 EasyAccounts 前端完成。
{% endhint %}

## 相关链接

- 仓库：[EasyAccounts-Skills](https://github.com/QingHeYang/EasyAccounts-Skills)
- OpenClaw 主项目：[OpenClaw](https://github.com/QingHeYang/EasyAccounts-Skills)
- 问题反馈：在仓库 [Issue](https://github.com/QingHeYang/EasyAccounts-Skills/issues) 区提交
