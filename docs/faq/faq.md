# 常见问题

### Q1: 为什么我打开页面后，会显示这个
<img src="faq/image/q1.png" width="40%" />

A: 请使用 10669 端口访问记账页面，10670 端口访问的是后台Api，SwaggerApi  


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
A: 请检查是否有如下配置项在nginx容器中
```shell
    environment:
      - API_BASE_URL=http://{IP}:10670 
```

其中{IP}为server的ip地址，一般是本机ip地址，或者你云服务器的域名  

### Q4: 外部数据库连接无反应  
A: 
1. 请确定`server`容器中下列字段配置正确，且外部数据库已经开启远程连接   
- `- MYSQL_HOST`
- `- MYSQL_PORT`
- `- MYSQL_USERNAME`
- `- DB_PASSWORD`

2. 在我开发写代码的时候，数据库结构不会自动生成  
所以请手动导入`yd_jz_base.sql`文件到外部数据库中  
**导入后命名数据库`yd_jz`**，非此数据库名会导致程序无法连接数据库  


### Q5: 怎么我的腾讯云、阿里云服务器无法访问记账页面？  
A: 请阿里云检查Ecs安全组,腾讯云检查防火墙规则  
确保10669、10670端口是开放的，如果外部访问数据库，还需要确保数据库端口10668是开放的  
如果是家里的服务器访问不通，请自行解决网络问题

### Q6: FNOS如何部署？  
A: 部署前请先阅读[部署文档](deploy/deploy.md)，然后在看[飞牛云平台部署](platform/fnos.md)  

### Q7: 会维护多久？  
A: 项目会长期维护

### Q8: 是否会收费？
A: 不会  

### Q9: 是否会要github or gitee 的star?  
A: 会，你既然看到这里了，打劫！ 把star交出来！