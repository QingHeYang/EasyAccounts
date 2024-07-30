# 2.1.0  
- 修复了一些bug
- 快记模板  
- 绑定分类与收支功能  
- 搜索功能

升级方法：
- 请先备份数据库

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