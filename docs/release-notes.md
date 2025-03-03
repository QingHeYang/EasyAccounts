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
