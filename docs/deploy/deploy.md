# EasyAccounts项目部署

下面内容针对Debian系统的Docker部署\
更多平台部署请参考[平台部署](../platform/ubuntu\&windows.md)

## 环境准备

安装Docker和Docker-Compose，具体安装方法请自行搜索，不再赘述\
~~可以只部署Docker，例如群晖小伙伴可能没有compose~~(目前无法支持群晖，环境必备compose)

## 项目代码下载

项目具有两套地址，自行选择下载，项目内容是同步的

* Github: [https://github.com/QingHeYang/EasyAccounts](https://github.com/QingHeYang/EasyAccounts)
* GitCode: [https://gitcode.com/Silas_Kafka/EasyAccounts](https://gitcode.com/Silas_Kafka/EasyAccounts)

> 注：原码云（Gitee）地址已迁移至 GitCode

下载项目

Github:

```shell
git clone https://github.com/QingHeYang/EasyAccounts.git
```

GitCode:

```shell
git clone https://gitcode.com/Silas_Kafka/EasyAccounts.git
```

## 关于国内镜像

{% hint style="warning" %}
**重要说明**：从 2.6.0 版本起，无法继续提供国内镜像服务。

阿里云容器镜像服务已禁止个人用户上传新镜像，需要开通企业版才能继续使用，鄙人没那个实力。

如果有朋友可以提供镜像服务，万分感谢！
{% endhint %}

## 关于数据库初始化

{% hint style="success" %}
**2.6.0 版本起无需手动初始化数据库**

数据库初始化脚本已内置到 MySQL 镜像中，首次启动会自动完成初始化。

如果是从旧版本恢复数据库，请参考 [数据备份与恢复](../backup/backup.md)
{% endhint %}

## 配置项目

项目配置文件在[docker-compose.yml](https://github.com/QingHeYang/EasyAccounts/blob/main/docker-compose.yml)

项目配置文件分为 **4 个容器**（v2.7.0 起 webhook 已废弃）：

* db: 数据库容器
* nginx: 前端容器
* server: 后端容器（内置邮件发送，原 webhook 功能并入）
* ai: AI智能助手容器（可选）

## 启动项目

```shell
cd EasyAccounts
docker compose up -d
```

## 项目访问

**记账系统：http://{你的IP/域名}:10669**

首次访问需要注册账号


* Swagger 接口文档：http://{你的IP/域名}:10670/docs ，需要在 compose 中开启 server 端口映射才能访问
* 生成的 Excel、SQL 文件：http://{你的IP/域名}:10669/resources/

## 项目端口说明

* nginx容器：10669 (唯一对外暴露端口，记账页面 + 反向代理)

> 2.6.0 版本起，server、webhook、db 容器不再对外暴露端口，所有请求通过 nginx 反向代理

## 配置项目(可选)

### server容器配置

```yaml
- DB_PASSWORD=easy_accounts               # 数据库密码
```

{% hint style="info" %}
**v2.7.0 配置迁移**：以下配置已从 compose 环境变量下沉到前端「**系统设置**」UI，启动后在 Web 端配置，**改完立即生效，无需重启容器**：

| 旧环境变量 | 现位置 |
|-----------|--------|
| `SQL_BACKUP_TIME` | 系统设置 → 备份 |
| `ENABLE_LOGIN` | 系统设置 → 鉴权 |
| `EXPIRED_TIME` | 系统设置 → 鉴权 |
| `SINGLE_LOGIN` | 系统设置 → 鉴权 |
| webhook 容器 `SMTP_*` | 系统设置 → 邮件 |
{% endhint %}

### ai容器配置

* ai容器：详见[AI智能助手](ai.md)

### 数据库配置

如果不额外修改compose数据库相关的内容，使用默认数据库配置，数据库配置如下：

1. (**默认**)直接使用compose内部Mysql数据库：

* db容器：

```yaml
- MYSQL_ROOT_PASSWORD: easy_accounts # 数据库root密码
```

* server容器：

```yaml
- DB_PASSWORD=easy_accounts     # 数据库密码，与上方db容器的root密码一致
```

2.(可选)**自行配置外部Mysql数据库**：

* server容器：

```yaml
- MYSQL_HOST                    # 数据库地址
- MYSQL_PORT                    # 数据库端口
- MYSQL_USERNAME                # 数据库用户名
- DB_PASSWORD=easy_accounts     # 数据库密码
```

删除掉server容器如下内容：

```yaml
depends_on:
    - db
```

## 启动后文件结构

（待补充）
