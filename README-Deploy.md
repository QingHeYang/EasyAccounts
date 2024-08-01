# EasyAccounts
**中文记账软件**  
EasyAccounts是一款中文记账软件，主要的作用是简易记账  
特色功能有，生成Excel账单，定时备份数据库、账单数据  
| 项目部署 ｜ [功能介绍](./README.md) |  

这是部署的B站视频地址：[【开源记账软件 EasyAccounts 部署教程-哔哩哔哩】 ](https://b23.tv/a09YbJa)
 
## 项目说明  
该项目源自2021年10月，起初只是因为类似网易有钱之类的账单App下架，家人没有的用了，所以决定自己开发一款记账软件，详情不另做说明  
做该项目的起因是当初使用很多国内的互联网记账软件，结果因为经营不善，亦或者政策缘故，导致软件停止维护，最终账单丢失    
本意是给家人使用，但由于我在各个论坛逛的时候，发现还是有部分人有需求的，就花了段时间开源该项目    
### 项目架构  
项目采用前后端分离  
- 后端: Java Spring Boot
- 数据库： Mysql
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
如果你下载不下来，可以尝试使用码云的镜像  
```shell
git clone https://gitee.com/qingheyang/EasyAccounts.git
cd EasyAccounts
```


**下载完成后，进入项目目录，搭建数据库目录**   
**这步很重要，不要忽略**  
```shell
mkdir -p Database/init
cp Database/base_sql/yd_jz_base.sql Database/init/yd_jz_base.sql
```

Tips：补救措施
> 如果**上一步没有**做复制数据库进行初始化，请做如下操作：  
> ```shell  
> #首先停掉compose
> docker-compose down
> #删除数据库数据
> sudo rm -rf Database/data  
> ```
> 然后执行上一步复制数据库命令

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
详见docker-compose.yml文件:[docker-compose.yml](./docker-compose.yml)  
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

> Tips: SQL备份时间corn表达式，可以参考这个网站：[在线corn表达式生成](https://www.bejson.com/othertools/cron/)  

### 启动项目  
1. 推荐使用Compose启动项目  
```shell
docker-compose up -d
```  
> 如果你在中国大陆，可能存在拉不下镜像的情况，这里我提供里阿里云的镜像compose文件  
> ```shell
> docker-compose -f docker-compose-chinese.yml up -d
> ``` 
> 如果你有条件使用梯子等工具，可以使用原始的compose文件，速度会更快，而且阿里云镜像这块我可能更新不够及时  

2. 如果不使用Compose，可以使用Docker启动项目  
```shell
sudo chmod u+x start-easyaccounts.sh
./start-easyaccounts.sh
```
3. 根据bash脚本，自行启动项目  

### 启动后目录结构  
```shell
 (base) root@tesla-t4:~/EasyAccounts# tree -L 2
 .
├── Database
│   ├── data                      # 数据库数据,不要修改,自动创建
│   └── init                      # 数据库初始化文件
├── docker-compose-chinese.yml    # 阿里云镜像compose文件
├── docker-compose.yml            # docker hub compose文件
├── LICENSE
├── README.md
├── Resource                      # 资源文件目录
│   ├── excel                     # excel文件目录，自动生成的目录
│   └── sql                       # sql备份文件目录，自动生成的目录
├── Server
│   └── logs                      # 日志文件目录
├── start-easyaccounts-chinese.sh # docker-client阿里云镜像启动脚本
├── start-easyaccounts.sh         # docker-client启动脚本
├── update-docker-chinese.sh      # 阿里云镜像更新脚本
├── update-docker.sh              # docker hub 更新脚本
└── WebHook
    ├── hook.log                  # Webhook日志文件
    ├── __pycache__               # Webhook缓存文件,自动生成的目录，不要修改
    ├── webhook-email.py          # Webhook邮件发送脚本
    └── webhook.py                # Webhook脚本
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

## 项目备份恢复
倘若你服务器出现错误，或者要重新部署，不要着急。  
你是用最后一次保存备份的sql文件，放到DataBase/init 中，删掉DataBase/data中的所有文件，然后重启compose即可。  
这就是为什么我强烈建议你定时保存备份的sql文件，因为这个文件可以让你的数据永远不会丢失。
  
## 日志查看  
- 服务端日志：Server/logs/  
- WebHook日志：WebHook/hook.log

## 项目更新  
更新建议：  
1. 备份数据库  
2. 备份excel文件  
3. `git pull`  
4. 选择使用的compose文件，down  
5. 执行对应的update升级脚本  
6. 启动compose