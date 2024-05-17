#!/bin/bash

# 创建网络，确保所有容器可以在同一个网络内通信
docker network create easy_accounts_net

# 启动 MySQL 数据库
# - 持久化 MySQL 数据
# - 初始化脚本在第一次数据库启动时运行
# - 设置字符集和校对以支持 UTF-8
docker run -d \
  --name easy_accounts_db \
  --network easy_accounts_net \
  --restart always \
  -p 10668:3306 \
  -e TZ=Asia/Shanghai \
  -e MYSQL_ROOT_PASSWORD=easy_accounts \
  -e MYSQL_DATABASE=yd_jz \
  -v "$(pwd)/Database/data:/var/lib/mysql" \
  -v "$(pwd)/Database/init:/docker-entrypoint-initdb.d" \
  mysql:8.0.31 \
  --default-authentication-plugin=mysql_native_password \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_general_ci \
  --explicit_defaults_for_timestamp=true \
  --lower_case_table_names=1

# 启动 Nginx 服务
# - Nginx 作为反向代理，转发请求到后端服务
# - 配置 API_BASE_URL 环境变量以指向后端服务地址
docker run -d \
  --name easy_accounts_nginx \
  --network easy_accounts_net \
  --restart always \
  -p 10669:80 \
  -e API_BASE_URL=http://{ip}:10670 \
  -v "$(pwd)/Resource:/usr/share/nginx/html/resources" \
  775495797/easyaccounts-nginx:latest

# 启动服务端
# - 配置数据库密码和 SQL 备份时间
# - 映射备份和 Excel 文件目录以及日志文件目录
docker run -d \
  --name easy_accounts_server \
  --network easy_accounts_net \
  --restart always \
  -p 10670:8081 \
  -e DB_PASSWORD=easy_accounts \
  -e SQL_BACKUP_TIME='00 00 22 * * ?' \
  -v "$(pwd)/Resource/sql:/Ledger/backup" \
  -v "$(pwd)/Resource/excel/month:/Ledger/excel/month" \
  -v "$(pwd)/Resource/excel/screen:/Ledger/excel/screen" \
  -v "$(pwd)/Server/logs:/Ledger/logs" \
  775495797/easyaccounts-server:latest

# 启动 Webhook 服务
# - Webhook 用于处理外部事件，日志文件记录事件处理结果
docker run -d \
  --name easy_accounts_webhook \
  --network easy_accounts_net \
  --restart always \
  -p 10671:8083 \
  -v "$(pwd)/WebHook:/app" \
  -v "$(pwd)/WebHook/webhook.py:/app/webhook.py" \
  -e LOG_FILE=/app/hook.log \
  775495797/easyaccounts-webhook:latest
