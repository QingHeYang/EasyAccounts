# 常见问题

### Q1: 为什么我打开页面后，会显示这个

![](faq/image/q1.png)

A: 请使用 **10669** 端口访问记账页面（nginx 前端）。

v2.6.0 起，server/db/webhook 等容器不再对外暴露端口，所有请求都通过 10669 上的 nginx 反向代理。如果你看到这个 Swagger 风格的页面，说明你访问的是后端 api 端口，不是前端页面。

### Q2: 忘记密码怎么办

A: 按如下操作重置密码

1. 找到server，确保有如下配置项在，没有就添加上

```shell
    volumes:
      - ./Server/auth:/Ledger/auth
```

2. 进入对应的外部映射目录，找到auth文件夹，删除其中的secret.key文件
3. 刷新界面，重新注册即可，windows需要重启compose

### Q2补充：怎么每次重启都要重新注册？

A： 同上第一条，需要数据持久化到外部，映射出去就好了

### Q3: 打开记账首页后，卡在主页，顶部提示Network Error

A:

**v2.6.0 及以上版本**：所有请求通过 nginx 反向代理，**无需任何额外配置**。如果你是从 v2.4.x 升级，请删除 nginx 容器里残留的 `API_BASE_URL` 环境变量后重启。

**v2.4.x 老版本**（已不再维护）：需要配置 nginx 容器的 `API_BASE_URL=http://{IP}:10670`。建议升级到最新版本。

### Q4: 外部数据库连接无反应

A:

1. 请确定`server`容器中下列字段配置正确，且外部数据库已经开启远程连接

* `- MYSQL_HOST`
* `- MYSQL_PORT`
* `- MYSQL_USERNAME`
* `- DB_PASSWORD`

2. v2.6.0 版本起，数据库初始化脚本已内置到 MySQL 镜像，使用 EasyAccounts 自带 MySQL 时**无需手动导入**；如使用外部数据库，请手动导入 `yd_jz_base.sql` 到外部数据库，**数据库名必须为 `yd_jz`**

### Q5: 怎么外网访问不到记账页面？（云服务器 / 家庭环境 / NAS）

A:

**云服务器**：阿里云检查 ECS 安全组，腾讯云检查防火墙规则，**确保 10669 端口对外开放**。

**家庭环境 / NAS**：路由器把 **10669 端口** 映射到外网即可。

v2.6.0 起 server/db 容器不再对外暴露端口，**只需开放 10669 一个端口**，不再需要开 10670 / 10668 等。从 v2.4.x 升级的老用户，请同时删掉 nginx 容器残留的 `API_BASE_URL` 环境变量。

### Q6: FNOS如何部署？

A: 部署前请先阅读[部署文档](deploy/deploy.md)，然后在看[飞牛云平台部署](platform/fnos.md)

### Q7: v2.7.0 升级后邮件/备份/登录配置去哪了？

A: **v2.7.0 起这些配置全部迁移到了前端「系统设置」**，原 `docker-compose.yml` 中的 `webhook:` 服务块和 `SMTP_*`、`SQL_BACKUP_TIME`、`ENABLE_LOGIN`、`EXPIRED_TIME`、`SINGLE_LOGIN` 等环境变量都已废弃。

- **邮件 SMTP** → 系统设置 → 邮件
- **备份时间** → 系统设置 → 备份
- **登录开关 / 过期时间** → 系统设置 → 鉴权

改完立即生效，**无需重启容器**。详见 [v2.7.0 升级说明](version/v2.7.0.md)。

### Q8: 用了反向代理后，AI 助手连不上 / 一直转圈？

A: 反向代理需要支持 WebSocket。请确保 nginx 配置里有 WebSocket Upgrade 三件套：

```nginx
location / {
    proxy_pass http://easy_accounts_nginx:80;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Caddy / Traefik 默认支持 WebSocket，通常无需额外配置。详见 issue [#23](https://github.com/QingHeYang/EasyAccounts/issues/23)。

### Q9: 套了反代后登录被频繁踢出 / 鉴权异常？

A: nginx 默认会丢弃带下划线的 header，可能影响登录。在 nginx 配置加：

```nginx
underscores_in_headers on;
```

### Q10: 项目说开源，但源码仓库为什么没有最新版本的代码？

A: 项目坚持开源，**源码会更新，只是相对发布版本会延迟一段时间**。

原因是新版本通常包含较多结构调整和重写，需要先在内部充分自测、调优、修 bug，避免开源出来一份"半成品"误导贡献者或让用户基于不稳定的代码二次开发。等版本在生产环境跑稳了，会同步推到开源仓库。

如果你想参与贡献或基于源码二次开发，请耐心等待开源仓库同步到最新版本。

### Q11: 我想参与项目贡献，可以提 PR 加新功能吗？

A: **本项目仅接受 Bug 修复类 PR，不接受新功能贡献**。

这是为了对已有用户负责：

- 新功能涉及产品定位、用户体验、数据模型一致性等多方面取舍，需要从全局规划
- 没有充分讨论的新功能合并进来，可能与后续版本的设计冲突，给老用户带来破坏性升级
- 对开源记账软件来说，"稳定"比"功能丰富"更重要

**欢迎以下贡献**：

- ✅ Bug 修复（含线上问题、文档错误、配置坑点）
- ✅ Issue 反馈（功能建议、使用问题、改进想法）
- ✅ 文档完善、翻译、教程
- ✅ 平台部署测试反馈（FNOS / 群晖 / 各类 NAS）
- ❌ 直接提新功能 PR

如果你有好的功能想法，欢迎在 GitHub Issue 区讨论，合适的会在后续版本中加入。

### QN: 会维护多久？

A: 项目会长期维护

### QN+1: 是否会收费？

A: 不会

### QN+2: 是否会要github or gitee 的star?

A: 会，你既然看到这里了，打劫！ 把star交出来！
