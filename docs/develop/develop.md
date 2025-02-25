# 源码说明

## 地址
项目源码在这里：https://github.com/QingHeYang/EasyAccountsOpenSource

## 主要目录结构(有删减)
```bash
.
├── CONTRIBUTING.md             # 贡献指南
├── README.md                     
├── Server                      # 服务端文件夹
│   ├── Dockerfile                # Dockerfile
│   ├── excel_template            # 账单模板
│   │   ├── analysis_excel.xls    # 分析账单模板
│   │   ├── auto_excel.xls        # 月度账单模板
│   │   └── screen_excel.xls      # 筛选账单模板
│   ├── make_jar.sh               # 打包脚本，制作jar&docker镜像
│   └── YD_JZ                     # 服务端源码
│
├── Web                         # 前端文件夹
│   ├── Dockerfile                # Dockerfile
│   ├── make_nginx.sh             # 打包脚本，制作nginx镜像
│   ├── nginx                     # nginx文件夹
│   │   └── default.conf          # nginx配置文件
│   └── ydjz_web                  # 前端源码
│       └── public                # 公共文件夹
│           └── config.js         # 配置文件，本地运行修改IP链接后台使用
│
└── WebHook                      # WebHook文件夹
    ├── Dockerfile                # Dockerfile
    ├── make_webhook.sh           # 打包脚本，制作webhook镜像
    ├── requirements.txt          # 依赖文件
    └── webhook.py                # webhook源码
```  

## 项目说明

### 服务端  
- 服务端语言：Java
- 服务端框架：SpringBoot
- 服务端数据库：MySQL
- 服务端日志：Log4j  
- 服务端构建工具：Maven
- 服务端运行环境：JDK11
- 服务端部署方式：Docker  
- swagger文档：http://{YOUR_IP}:8085/swagger-ui/index.html  
  
- 本地运行端口号：8085
- docker运行端口号：10670
- MySQL版本：8.0.31

配置文件：
- application.properties            # 本地运行配置文件
- application-dev.properties        # 开发环境配置文件
- application-server.properties     # 服务器环境配置文件
- application-windows.properties    # 本地windows环境配置文件  

本地运行指南：  
- 选择本地运行配置文件：application-windows.properties
- 修改数据库链接：
```bash
spring.datasource.url=jdbc:mysql://{YOUR_MYSQL_IP}:3306/easy_accounts?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
spring.datasource.username={YOUR_MYSQL_USERNAME}
spring.datasource.password={YOUR_MYSQL_PASSWORD}
```

制作镜像指南：  
- 运行脚本：`./make_jar.sh`，如需更换tag，请自行修改

### 前端
- 前端语言：Vue
- 前端框架：Vue3
- 前端构建工具：VueCli
- 前端组件：Vant4
- 前端运行环境：Node.js 18-22版本均可
- 前端部署方式：Docker

- 本地运行端口号：8081
- docker运行端口号：10669

本地运行指南：
- 修改后端链接：public/config.js  
- 字段：`apiBaseUrl: "${YOUR_IP}:8085"`

制作镜像指南：  
- 运行脚本：`./make_nginx.sh`，如需更换tag，请自行修改

### WebHook
- 服务端语言：Python
- 服务端框架：FastAPI
- 服务端运行环境：Python3.10
- 服务端部署方式：Docker

- 本地运行端口号：8083
- docker运行端口号：10671

本地运行指南：
1. 安装requirements.txt依赖：`pip install -r requirements.txt`  
2. 运行webhook.py：`uvicorn webhook:app --host 0.0.0.0 --port 8083`

制作镜像指南：  
- 运行脚本：`./make_webhook.sh`，如需更换tag，请自行修改  

## 项目开发建议  
### 轻度开发  
基于WebHook开发  
1. 使用已有swagger文档，开发新功能，一般可以用查询、筛选等功能
2. 在已有的webhook中调用对应的接口即可，使用python编码  
3. 打包镜像：`./make_webhook.sh`，如需引用额外的python包，修改requirements.txt文件  

轻度开发适用场景：1. 创新性开发、2. 不变更主体逻辑、3. 映射文件后方便修改。

需要能力：  
- 轻度python编码(AI辅助即可)
- 使用docker
- 阅读swagger文档

### 中度开发  
基于服务端、前端开发  
1. 使用源码开发，开发对应功能，不变更数据库，例如修改登录等功能 
2. 基于服务端、前端源码进行修改
3. 打包镜像：`./make_nginx.sh`、`./make_jar.sh`  

中度开发适用场景：1.原有记账逻辑不符合需求、2.有修改界面等需求

需要能力：  
- java编码(修改服务端)
- 使用docker
- vue编码(修改前端)

### 重度开发  
基于服务端、前端开发  
1. 使用源码开发，开发对应功能，变更数据库，例如新增数据库表等 
2. 打包镜像：`./make_jar.sh`  

重度开发适用场景：1. 原有记账逻辑不符合需求、2. 有新增数据库表等需求

需要能力：  
- java编码(修改服务端)
- 使用docker
- vue编码(修改前端)  

## 贡献指南
[点击这里查看贡献指南](develop/CONTRIBUTING.md)  
>Tips: 仅接受轻度、中度开发PR

## 安全声明  
本项目是开源项目，你可以自由使用，但是请不要将这个项目用于商业用途，无法支撑起商业用途   
本项目没有上传任何使用者的数据，如果你发现有上传数据的行为，请及时联系我  
欢迎审查代码  

## 开发者的话
这个项目是我业余时间开发的，可能会有很多不完善的地方  
我本职是一个Android开发工程师，对于前端、后端、数据库等方面的知识了解不多  
所以代码并不是很规范，还望谅解  