# 飞牛OS部署  
> 部署前提示：
> 飞牛云本质上是一个Debian系统，所以项目配置与[部署文档](/deploy/deploy.md)基本一致，只是在构建部分有所不同，所以请先阅读[部署文档](/deploy/deploy.md)

## 项目准备  
> 1. 项目文件  
> 2. Fnos网页端  
> 3. Fnos后端  

## 下载并修改项目  
1. 下载项目到本地，无论是什么系统，下载完后解压，此操作无需在Fnos上做，可以在windows或者别的操作系统中执行    
<img src="/image/fnos-download.png" width="75%" />  

2. 修改项目内容（v2.6.0+ 已无需此步骤）

> **v2.6.0 及以上版本**：数据库初始化文件已内置到 MySQL 镜像中，新用户无需手动复制 SQL 文件，直接启动即可。
>
> **老用户恢复数据**：可使用页面恢复功能（v2.6.1+），或参考 [数据恢复文档](/backup/backup.md)  


3. （可选）老用户可以选择将自己的docker-compose.yml替换掉新下载项目的对应compose文件  

> Tips:如果使用曾经的项目文件夹也可以，请务必将`./Database/data`文件夹删除掉！！如果项目部署失败，也需要删除掉这个文件夹！  

## 上传项目  
1. 选择刚才修改好文件夹并上传  
<img src="/image/fnos-upload.png" width="75%" />  

2. 上传后结果  
<img src="/image/fnos-upload-finish.png" width="75%" />  

## 数据库文件提权  
### 去Fnos后台登录  
<img src="/image/fnos-backup.png" width="75%" />  

### 找到自己刚才上传的文件夹的位置  
注意文件夹名称可能不是EasyAccounts-main
```
sudo find / -type d -name "EasyAccounts-main" 2>/dev/null 
```  
执行过程会要登录密码  
<img src="/image/fnos-find.png" width="75%" />  

进入到最后一个`/vol1/1000/EasyAccounts-main`中，前几个也同样可以进去，但是保存位置确实在最后一个  
```
cd vol1/1000/EasyAccounts-main  
ll
```

### 提权  
```
sudo chown -R 999:999 ./Database/init  
```
执行后进入`Databse`文件夹确认权限  
```
ll
```
看到如下则提权成功  
<img src="/image/fnos-primission.png" width="75%" />    

## 部署构建  
### 部署  
回到浏览器  
<img src="/image/fnos-docker.png" width="75%" /> 
<img src="/image/fnos-choose.png" width="75%" /> 
<img src="/image/fnos-compose.png" width="75%" /> 

### 修改compose

将 `docker-compose.yml` 的内容复制到项目构建框中

<img src="/image/fnos-compose-deploy.png" width="75%" />

按照标准[部署文档](/deploy/deploy.md) 修改 compose 对应的内容，此处不再赘述

> **注意**：从 v2.6.0 起，国内镜像（docker-compose-chinese.yml）已停止支持  

### 构建  
启动构建  
<img src="/image/fnos-build.png" width="75%" /> 

当db容器日志中出现如下内容表示数据库成功  
<img src="/image/fnos-mysql-success.png" width="75%" /> 

当server容器日志中出现如下内容表示后台成功  
<img src="/image/fnos-server-success.png" width="75%" /> 
