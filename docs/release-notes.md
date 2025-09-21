# Relase-Notes

## 升级方法

升级方法一般固定，只有在特殊情况下才会有变化，如有变化会在版本更新说明中说明。 升级方法：

* 请先备份数据库

使用阿里云镜像部署（docker-compose-chinese.yml）升级：

```bash
# 停止容器
docker-compose -f docker-compose-chinese.yml down
```

```bash
# 增加权限
chmod +x update-docker-chinese.sh
```

```bash
# 更新镜像
./update-docker-chinese.sh
```

```bash
# 启动容器
docker-compose -f docker-compose-chinese.yml up -d
```

使用Docker-Hub部署（docker-compose.yml）升级：

```bash
# 停止容器
docker-compose down
```

```bash
# 增加权限
chmod +x update-docker.sh
```

```bash
# 更新镜像
./update-docker.sh
```

```bash
# 启动容器
docker-compose -f docker-compose.yml up -d
```

***

## 2.5.0(AI+图片附件)

* fixbugs
  * 修复追加账单的时候，偶现的小数点后多位问题
* 新增功能
  * 新增账单明细附件功能功能，一笔明细可以附带三张照片
* 重要特性
  * 增加AI功能，通过配置自己的api-key，可以使用对应平台的llm进行账单问答，快速记账，修改账目
*   技术特性

    * 增加nginx容器反向代理功能，摆脱BASE\_URL配置项



### compose变更字段

```
nginx:
    #environment: #删掉该行
    #    - API_BASE_URL=http://你的IP:10670 #删掉改行
```

```
server:
    volumes:
        - ./Resource/images:/Ledger/images # 新增图片上传文件目录
```

```
  # AI智能助手服务（可选）
  # 如果不想使用AI功能，可以删除或注释掉整个ai服务块
  ai:
    image: registry.cn-beijing.aliyuncs.com/easy_accounts/easyaccounts-ai:latest  # 此处使用阿里云镜像
    container_name: easy_accounts_ai
    restart: always
    environment:
      # LLM 配置（请替换为您的实际配置）
      # 默认使用 OpenAI API 配置，您需要：
      # 1. 前往 https://platform.openai.com 申请 API Key
      # 2. 将下面的 sk-your-openai-key-here 替换为您的实际密钥
      
      - LLM_EASY_ACCOUNTS_API_KEY=sk-your-openai-key-here  # 替换为您的 OpenAI API Key
      - LLM_EASY_ACCOUNTS_URL=https://api.openai.com/v1
      - LLM_EASY_ACCOUNTS_MODEL=gpt-3.5-turbo
      
      # 国内可用的其他 LLM 服务配置示例：
      # 月之暗面 Kimi (推荐国内用户):
      #- LLM_EASY_ACCOUNTS_API_KEY=sk-your-kimi-key
      #- LLM_EASY_ACCOUNTS_URL=https://api.moonshot.cn/v1
      #- LLM_EASY_ACCOUNTS_MODEL=moonshot-v1-8k

      
    volumes:
      # 数据库持久化
      - ./AI/database:/app/koalaq_hub_python/resource/database
      # 日志文件映射
      - ./AI/logs:/app/logs
      # 自定义AI角色和指令（可选）
      - ./AI/小易.role:/app/koalaq_hub_python/resource/role/小易.role
      - ./AI/task.prompt:/app/koalaq_hub_python/resource/prompts/layers/task/easy_accounts_instructions.prompt
    
    depends_on:
      - server
    networks:
      - easy_accounts_net
```

## 2.4.0(含登录)

* fixbugs
  *
    1. 修复主页请求500错误，跨年后请求错误
  *
    2. 修复webhook发送邮件，多收件人可能发送失败问题
  *
    3. 生成历史月份Excel，报表中账户金额可以追溯
* 新增功能
  *
    1. 增加点击生成Excel报表后反馈，变为同步式等待
  *
    2. webhook修改逻辑判断
  *
    3. 重构总览界面，增加当年月度概览，账户详情转移至顶部
  *
    4. 记一笔按钮转移至明细（原流水）界面底部，可以拖动（电脑端可点击）
  *
    5. 筛选入口转移至原记一笔位置，主页不在提供筛选选项卡
  *
    6. 筛选默认开启备注搜索
* 重要特性
  *
    1. 增加登录功能，可以通过compose来开启关闭，compose不设置，默认关闭
  *
    2. 增加统计功能，原财务分析页面作废，统计功能为按分类统计汇总，按单项分类汇总，可按月查看单项分类明细
  *
    3. 分类管理增加不参与统计选项，不参与统计的分类不会出现在统计页面
* 技术特性
  *
    1. 增加外部Mysql数据库支持，可以通过compose来开启关闭，compose不设置，默认关闭
  *
    2. 前端VUE2->VUE3
  *
    3. 前端组件Vant2->Vant4

compose变新增字段：

```yaml
server:
    environment:
      - ENABLE_LOGIN=true                       # 是否启用登录功能，默认true 
      - EXPIRED_TIME=30                         # 登录过期时间，默认30分钟，单位分钟

    volumes:
      - ./Server/auth:/Ledger/auth              # 登录认证文件目录,需要映射，否则重启后会丢失用户名密码 
```

功能截图

## 2.1.1(无登录)

* 修复PC端无法点击按钮记账问题，恢复成顶部按钮

## 2.1.0

* 修复了一些bug
* 快记模板
* 绑定分类与收支功能
* 搜索功能
