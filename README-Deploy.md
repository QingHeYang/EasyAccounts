# EasyAccounts
**中文记账软件**  
EasyAccounts是一款中文记账软件，主要的作用是简易记账  
特色功能有，生成Excel账单，定时备份数据库、账单数据  
| 项目部署 ｜ [功能介绍](./README.md) |  
 
## 项目说明  
该项目源自2021年10月，起初只是因为类似网易有钱之类的账单App下架，家人没有的用了，所以决定自己开发一款记账软件，详情不另做说明  
做该项目的起因是当初使用很多国内的互联网记账软件，结果因为经营不善，亦或者政策缘故，导致软件停止维护，最终账单丢失    
本意是给家人使用，但由于我在各个论坛逛的时候，发现还是有部分人有需求的，就花了段时间开源该项目    
### 项目架构  
项目采用前后端分离  
- 后端: Java Spring Boot
- 数据库： MariaDB
- 前端：VUE
- 部署：Docker/Docker-Compose

### 项目部署  
### 环境准备
安装Docker和Docker-Compose，具体安装方法请自行搜索，不再赘述，可以只部署Docker，例如群晖小伙伴可能没有compose  

### 下载项目代码  
```shell
git clone https://github.com/QingHeYang/EasyAccounts.git
cd EasyAccounts
```

**下载完成后，进入项目目录，搭建数据库目录**   
!!!这步很重要，不要忽略  
```shell
mkdir -p Database/init
cp Database/base_sql/yd_jz_base.sql Database/init/yd_jz_base.sql
```

搭建完后的目录可以看到如下文件  
```shell
 (base) root@tesla-t4:~/EasyAccounts# tree
.
├── Database
│   └── init
│       └── yd_jz.sql #数据库初始化文件
├── docker-compose.yml #docker-compose文件
├── LICENSE #开源协议
├── README.md 
├── start-easyaccounts.sh #Docker启动脚本
└── WebHook
    └── webhook.py #WebHook脚本
```
### 配置项目
compose文件如下：
```yaml
version: '3.8'

services:

  #数据库端，请勿分开部署Mysql与服务端，内部有网桥链接，分开部署会导致服务端无法连接数据库，请勿修改"db"服务的名称，否则会导致服务端无法连接数据库
  db:   
    restart: always
    container_name: easy_accounts_db
    image: mysql:8.0.31
    ports:
      - "10668:3306"
    environment:
      TZ: Asia/Shanghai
      MYSQL_ROOT_PASSWORD: easy_accounts #数据库root密码，自行修改，修改完需要修改Server中的数据库密码
      MYSQL_DATABASE: yd_jz #数据库名称，请勿修改
    volumes:
      - ./Database/data:/var/lib/mysql
      - ./Database/init:/docker-entrypoint-initdb.d
    command:
      --default-authentication-plugin=mysql_native_password
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --explicit_defaults_for_timestamp=true
      --lower_case_table_names=1
    networks:
      - easy_accounts_net

  nginx:
    restart: always
    container_name: easy_accounts_nginx
    image: 775495797/easyaccounts-nginx:latest
    ports:
      - "10669:80"
    environment:
      - API_BASE_URL=http://ip:10670 #此处务必填写Server 的ip地址与端口号 ，见59行
    volumes:
      #- ./Web/dist:/usr/share/nginx/html #如若需要自行修改前端，请将前端放置在Web/dist目录下，并解开此行注释
      #- ./Web/nginx/default.conf:/etc/nginx/conf.d/default.conf #如若需要自行修改nginx配置，请将配置文件放置在Web/nginx/default.conf目录下，并解开此行注释
      - ./Resource:/usr/share/nginx/html/resources #资源文件目录，此文件夹提供一个下载功能
    depends_on:
      - server
    networks:
      - easy_accounts_net

  server:
    restart: always
    container_name: easy_accounts_server
    image: 775495797/easyaccounts-server:latest
    environment:
      - DB_PASSWORD=easy_accounts #数据库密码,默认easy_accounts
      - SQL_BACKUP_TIME=00 00 22 * * ? # SQL备份时间 corn表达式,默认每天晚上10点
    volumes:
      - ./Resource/sql:/Ledger/backup #数据库备份文件目录
      - ./Resource/excel/month:/Ledger/excel/month #excel 生成月度账单文件目录
      - ./Resource/excel/screen:/Ledger/excel/screen #excel 生成筛选账单文件目录
      - ./Server/logs:/Ledger/logs #日志文件目录
      #- ./Server/config/:/Ledger/config #配置文件目录
      #- ../EasyAccountsSource/Server/YD_JZ/target/YD_JZ-SNAPSHOT.jar:/Ledger/app/YD_JZ-SNAPSHOT.jar #服务端jar包，如若需要自行修改，请将jar包放置在Server/app目录下，并修改此行
    ports:
      - 10670:8081 #左侧映射出去的端口号为服务端口号 默认10670
    depends_on:
      - db
    networks:
      - easy_accounts_net
  
  webhook:
    image: 775495797/easyaccounts-webhook:latest
    container_name: easy_accounts_webhook
    ports:
      - "10671:8083"
    volumes:
      - ./WebHook:/app/
      #- ./WebHook/webhook-tools.py:/app/webhook.py
      - ./WebHook/webhook.py:/app/webhook.py
    environment:
      - LOG_FILE=/app/hook.log
    networks:
      - easy_accounts_net
networks:
  easy_accounts_net:

```
必要的配置项有：
- API_BASE_URL=http://ip:port #此处务必填写Server 的ip地址与端口号  
因为项目是前后端分离的，前端需要知道后端的地址，所以需要填写后端的地址  

可选配置项有：
- 端口号可以自行修改，但是需要保证端口号不冲突
- 数据库密码可以自行修改，但是需要保证数据库密码与Server中的数据库密码一致
- SQL备份时间 corn表达式，可以自行修改，但是需要保证corn表达式正确
- 数据库备份文件目录，excel 生成月度账单文件目录，excel 生成筛选账单文件目录，日志文件目录，配置文件目录，服务端jar包，都可以自行修改，但是需要保证路径正确

定制化开发（不建议自行开发）：
- 如果需要自行修改前端，请将前端放置在Web/dist目录下，并解开此行注释
- 如果需要自行修改nginx配置，请将配置文件放置在Web/nginx/default.conf目录下，并解开此行注释
- 如果需要自行修改服务端jar包，请将jar包放置在Server/app目录下，并修改此行

### 启动项目  
1. 推荐使用Compose启动项目  
```shell
docker-compose up -d
```
2. 如果不使用Compose，可以使用Docker启动项目  
```shell
chmod u+x start-easyaccounts.sh
./start-easyaccounts.sh
```
3. 根据bash脚本，自行启动项目  

### 启动后目录结构  
```shell
 (base) root@tesla-t4:~/EasyAccounts# tree -L 2
 .
├── Database
│   ├── data #数据库数据,不要修改,自动创建
│   └── init #数据库初始化文件
├── docker-compose.yml
├── LICENSE
├── README.md
├── Resource #资源文件目录
│   ├── excel #excel文件目录，自动生成的目录
│   └── sql #sql备份文件目录，自动生成的目录
├── Server
│   └── logs #日志文件目录
├── start-easyaccounts.sh
└── WebHook
    ├── hook.log #Webhook日志文件
    ├── __pycache__ #Webhook缓存文件,自动生成的目录，不要修改
    └── webhook.py
```

### 项目服务说明
- 服务端：http://ip:10670 ，用于提供后端服务
- 前端：http://ip:10669 ，用于提供前端服务
- WebHook：http://ip:10671 ，用于提供WebHook服务，生成的excel、sql的时候，会主动调用该服务，具体功能请查看WebHook/webhook.py，可以自行修改这个代码，修改完后，重启compose即可生效，文件会传输到WebHook接口里，可以自行开发
- 数据库：http://ip:10668 ，用于提供数据库服务

### 项目访问
- 记账系统：访问 http://ip:10669 ，即可进入记账系统，进去之后是空白的，可能会报错，因为没有数据，需要自行添加数据，点击下面的“总览”、“流水”、“设置”添加数据，然后记账即可
- 服务端swagger：http://ip:10670/swagger-ui.html ，可以查看服务端的接口文档
- 生成的excel、sql文件：http://ip:10669/resources ，可以查看生成的excel、sql文件，可以自行下载
