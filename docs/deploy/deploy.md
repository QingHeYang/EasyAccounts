# EasyAccounts项目部署

下面内容针对Debain系统的Docker部署  
更多平台部署请参考[平台部署](../platform/ubuntu&windows.md)

## 环境准备

安装Docker和Docker-Compose，具体安装方法请自行搜索，不再赘述\
~~可以只部署Docker，例如群晖小伙伴可能没有compose~~(目前无法支持群晖，环境必备compose)

## 项目代码下载

项目具有两套地址，自行选择下载，项目内容是同步的

* Github: [EasyAccounts:https://github.com/QingHeYang/EasyAccounts](https://github.com/QingHeYang/EasyAccounts)
* 码云: [EasyAccounts:https://gitee.com/qingheyang/EasyAccounts](https://gitee.com/qingheyang/EasyAccounts)

下载项目

github:

```shell
git clone https://github.com/QingHeYang/EasyAccounts.git
```

码云:

```shell
git clone https://gitee.com/qingheyang/EasyAccounts.git
```

## 数据库初始化

**这步很重要，不要忽略**

```shell
cd EasyAccounts
mkdir -p Database/init
cp Database/base_sql/yd_jz_base.sql Database/init/yd_jz_base.sql
```

搭建完后的目录如下：

```shell
root@VM-20-8-ubuntu:~/EasyAccounts# tree -I image
.
├── Database
│   ├── base_sql
│   │   └── yd_jz_base.sql
│   └── init                    # 数据库初始化文件夹
│       └── yd_jz_base.sql      # 数据库初始化文件
├── docker-compose-chinese.yml  # docker-compose 阿里云镜像
├── docker-compose.yml          # docker-compose dockerhub镜像
├── LICENSE
├── README-Deploy-Fnos.md
├── README-Deploy.md
├── README.md
├── Release-Note.md
├── update-docker-chinese.sh    # 更新docker-compose 阿里云镜像
├── update-docker.sh            # 更新docker-compose dockerhub镜像
└── WebHook                     # WebHook文件夹,用于发送邮件处理生成的文件
    ├── README.md
    ├── webhook-email.py        # 发送邮件脚本，自带发送邮件
    └── webhook.py              # WebHook脚本，可以自行处理文件，例如发送到企业微信、钉钉等
```

## 选择compose文件

项目提供两个compose文件，分别是：

* docker-compose.yml: 容器镜像在dockerhub上
* docker-compose-chinese.yml: 容器镜像在阿里云上\
  如果你在国内，不方便下载dockerhub镜像，可以选择docker-compose-chinese.yml

> Tips: 两个compose文件内容是一样的，只是镜像地址不同\
> 另外如果升级，请使用对应的升级脚本，如果要修改配置，请修改自己选择的compose文件

## 配置项目(必要)

项目配置文件在[docker-compose.yml](https://github.com/QingHeYang/EasyAccounts/blob/main/docker-compose.yml)

项目配置文件分为4个容器：

* server: 后端容器
* db: 数据库容器
* nginx: 前端容器
* webhook: 处理生成的报表与备份sql的容器

**必要的配置项**

* nginx容器：

```shell
- API_BASE_URL=http://{你的IP或者是域名}:10670    # 此处务必填写server的ip地址，一般是本机ip地址
```

> Tips: 此时，如果项目已经可以正常运行，可以不用修改其他配置项，直接启动项目

## 启动项目

使用docker-compose启动项目

```shell
docker-compose up -d
```

使用docker-compose-chinese.yml启动项目

```shell
docker-compose -f docker-compose-chinese.yml up -d
```

## 项目访问

* 记账系统：访问 http://ip:10669 ，如果开启了登录功能，需要先注册账号，然后登录
* SwaggerApi：http://ip:10670/swagger-ui.html ，可以查看服务端的接口文档
* 生成的excel、sql文件：http://ip:10669/resources/ ，可以查看生成的excel、sql文件，可以自行下载

{% hint style="warning" %}
&#x20;   [ 外网部署无法访问，点这里](../faq/wai-wang-fang-wen-faq.md)
{% endhint %}

## 项目端口说明

* server容器：10670
* nginx容器：10669 (记账页面)
* webhook容器：10671

## 配置项目(可选)

### server容器配置

```shell
- SQL_BACKUP_TIME=00 00 22 * * ?          # corn表达式，每天晚上10点备份数据库  
- ENABLE_LOGIN=true                       # 是否启用登录功能，默认true 
- EXPIRED_TIME=30                         # 登录过期时间，默认30分钟，单位分钟
```

> Tips: SQL备份时间corn表达式，可以参考这个网站：[在线corn表达式生成](https://www.bejson.com/othertools/cron/)

### webhook容器配置

* webhook容器：详见[WebHook](webhook.md)

### nginx容器配置

```shell
- ./Resource:/usr/share/nginx/html/resources    #资源文件目录，此文件夹提供一个下载功能
```

### 数据库配置

如果不额外修改compose数据库相关的内容，使用默认数据库配置，数据库配置如下：

1. (**默认**)直接使用compose内部Mysql数据库：

* db容器：

```shell
- MYSQL_ROOT_PASSWORD: easy_accounts # 数据库root密码
```

* server容器：

```shell
- DB_PASSWORD=easy_accounts     # 数据库密码，与上方db容器的root密码一致
```

2.(可选)**自行配置外部Mysql数据库**：

* server容器：

```shell
- MYSQL_HOST                    # 数据库地址
- MYSQL_PORT                    # 数据库端口
- MYSQL_USERNAME                # 数据库用户名
- DB_PASSWORD=easy_accounts     # 数据库密码
```

删除掉server容器如下内容：

```shell
depends_on:
    - db
```

## 启动后文件结构

```shell
root@VM-20-8-ubuntu:~/EasyAccounts# tree
.
├── Database
│   ├── base_sql
│   │   └── yd_jz_base.sql          # 数据库初始化文件，项目下载时自带
│   ├── data                        # 数据库数据文件夹，自动生成
│   └── init                        # 数据库初始化文件夹
│       └── yd_jz_base.sql          # 数据库初始化文件，通过命令复制过来的
├── docker-compose-chinese.yml      # docker-compose 阿里云镜像
├── docker-compose.yml              # docker-compose dockerhub镜像
├── image                           # 文档图片
├── LICENSE                 
├── README-Deploy-Fnos.md           
├── README-Deploy.md
├── README.md
├── Release-Note.md
├── Resource                        # 资源文件夹，可以通过nginx访问
│   ├── excel
│   │   ├── month                   # 月报表excel保存文件夹
│   │   └── screen                  # 筛选报表excel保存文件夹
│   └── sql
│       └── yd_jz_20240516_2200.sql # 数据库备份文件
├── Server
│   ├── auth                        # 登录认证文件夹
│   │   └── secret.key              # 登录认证key，删除掉可以重新注册
│   └── logs
│       ├── app.log                 # server容器日志
│       └── app-rolling.log
├── update-docker-chinese.sh        # 更新docker-compose 阿里云镜像
├── update-docker.sh                # 更新docker-compose dockerhub镜像
└── WebHook
    ├── hook.log                    # webhook容器日志
    ├── __pycache__
    │   └── webhook.cpython-310.pyc # webhook编译文件，勿删
    ├── README.md               
    ├── webhook-email.py            # 发送邮件脚本，自带发送邮件
    └── webhook.py                  # WebHook脚本，可以自行处理文件，例如发送到企业微信、钉钉等
```
