# AI 智能助手功能部署

EasyAccounts v2.5.0 新增了 AI 智能助手功能，可以通过对话方式进行记账查询和管理。  
本文档将指导你如何配置和部署 AI 服务。

> ⚠️ **重要提示**：AI 功能需要将您的查询数据发送到第三方 LLM 服务商进行处理，这是不可避免的。如果您对数据安全有顾虑，可以选择不启用此功能。

## 功能介绍

AI 智能助手"小易"是一个内置的财务管理助手，支持：
- **智能查询**：通过自然语言查询账单、余额、统计信息
- **语音记账**：说一句话就能记账，如"记一笔，今天吃饭花了50块"
- **数据分析**：询问收支情况、消费占比等分析问题
- **报表生成**：对话式生成Excel报表

## Compose配置

AI 服务已集成在 docker-compose 文件中，作为可选服务：

```yaml
ai:
    image: registry.cn-beijing.aliyuncs.com/easy_accounts/easyaccounts-ai:latest  # 阿里云镜像
    container_name: easy_accounts_ai
    restart: always
    environment:
      # LLM 配置（必填）
      - LLM_EASY_ACCOUNTS_API_KEY=sk-your-api-key  # 替换为您的 API Key
      - LLM_EASY_ACCOUNTS_URL=https://api.openai.com/v1
      - LLM_EASY_ACCOUNTS_MODEL=gpt-3.5-turbo
      
    volumes:
      # 数据库持久化
      - ./AI/database:/app/koalaq_hub_python/resource/database
      # 日志文件
      - ./AI/logs:/app/logs
      # 自定义配置
      - ./AI/小易.role:/app/koalaq_hub_python/resource/role/小易.role
      - ./AI/task.prompt:/app/koalaq_hub_python/resource/prompts/layers/task/easy_accounts_instructions.prompt
    
    depends_on:
      - server
    networks:
      - easy_accounts_net
```

## 配置步骤

### 1. 选择 LLM 服务提供商

AI 功能需要配置大语言模型（LLM）服务，支持以下提供商：

#### OpenAI（国际通用）
```yaml
- LLM_EASY_ACCOUNTS_API_KEY=sk-your-openai-key
- LLM_EASY_ACCOUNTS_URL=https://api.openai.com/v1
- LLM_EASY_ACCOUNTS_MODEL=gpt-3.5-turbo
```
申请地址：[https://platform.openai.com](https://platform.openai.com)

#### 月之暗面 Kimi（国内）
```yaml
- LLM_EASY_ACCOUNTS_API_KEY=sk-your-kimi-key
- LLM_EASY_ACCOUNTS_URL=https://api.moonshot.cn/v1
- LLM_EASY_ACCOUNTS_MODEL=moonshot-v1-8k
```
申请地址：[https://platform.moonshot.cn](https://platform.moonshot.cn)


### 2. 修改配置文件

编辑你选择的 compose 文件（docker-compose.yml 或 docker-compose-chinese.yml）：

```bash
# 编辑配置文件
vim docker-compose-chinese.yml

# 找到 ai 服务部分，修改环境变量
# 将 sk-your-openai-key-here 替换为你的实际 API Key
```

### 3. 自定义 AI 角色（可选）

AI 助手的性格和行为可通过配置文件自定义：

#### 编辑角色设定
文件位置：`AI/小易.role`
```yaml
role: 一个家庭小财务官              # AI扮演的角色
name: 小易                         # AI的名字
character: 活泼灵动，古灵精怪...    # 性格特征
```

#### 添加家庭信息
文件位置：`AI/task.prompt`
```markdown
## 特殊指导
我家有两个孩子，大宝和二宝
一辆特斯拉电车
每个月15号发工资
```

修改后需要重启 AI 服务：
```bash
docker restart easy_accounts_ai
```

## 启动服务

### 首次启动
如果是首次部署，直接启动所有服务：
```bash
docker-compose -f docker-compose-chinese.yml up -d
```

### 添加 AI 服务
如果已有 EasyAccounts 运行，只需启动 AI 服务：
```bash
docker-compose -f docker-compose-chinese.yml up -d ai
```

### 不使用 AI 功能
如果不需要 AI 功能，可以：
1. 注释或删除 compose 文件中的整个 ai 服务块
2. 或者启动时排除 AI 服务：
```bash
docker-compose -f docker-compose-chinese.yml up -d db nginx server webhook
```

## 验证部署

### 查看服务状态
```bash
docker ps | grep easy_accounts_ai
```

### 查看服务日志
```bash
docker logs easy_accounts_ai -f
```

### 测试 AI 功能
1. 打开 EasyAccounts 前端页面
2. 在明细页面找到 AI 助手入口（右下角浮动按钮）
3. 尝试对话："我的账户有多少钱？"

## 常见问题

### API Key 配置错误
**问题**：AI 服务启动失败，提示 API Key 无效  
**解决**：
1. 检查 API Key 是否正确
2. 确认 API 服务地址是否正确
3. 查看日志：`docker logs easy_accounts_ai`

### 网络连接问题
**问题**：国内无法访问 OpenAI API  
**解决**：
1. 使用国内 LLM 服务（如 Kimi、智谱）
2. 或配置代理服务器

### 响应速度慢
**问题**：AI 回复延迟高  
**解决**：
1. 选择更快的模型（如 gpt-3.5-turbo 比 gpt-4 快）
2. 使用国内服务减少网络延迟

### 费用问题
**说明**：AI 功能需要调用第三方 LLM 服务，会产生费用
- OpenAI：按 token 计费，约 $0.002/1K tokens
- Kimi：提供免费额度，超出后按量计费

## 使用示例

启动后，你可以这样与小易对话：

- **查询余额**："我微信还有多少钱？"
- **查看支出**："这个月吃饭花了多少？"
- **快速记账**："记一笔，今天加油200"
- **数据分析**："上个月哪项支出最多？"
- **生成报表**："导出这个月所有支出"

## 注意事项

1. **数据安全说明**：
   - AI 功能需要将查询数据发送到第三方 LLM 服务商（如 OpenAI、Kimi 等）
   - 您的账单数据会经过模型提供商的服务器处理，这是 AI 功能运行所必需的
   - 虽然大部分 LLM 服务商承诺不会存储用户数据，但数据传输是不可避免的
   - **如果您对数据安全有顾虑，建议不使用此功能，或仅用于非敏感数据查询**

2. **费用控制**：合理使用避免产生过多 API 调用费用
3. **模型选择**：不同模型的能力和价格不同，按需选择
4. **配置备份**：修改配置前建议备份原文件

## 相关链接

- [AI 功能说明](../../AI/README.md)
- [LLM 服务对比](https://platform.openai.com/docs/models)
- [问题反馈](https://github.com/QingHeYang/EasyAccounts/issues)