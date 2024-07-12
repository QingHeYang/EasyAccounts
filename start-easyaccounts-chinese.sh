#!/bin/bash

# 创建网络
echo "Creating network..."
docker network create easy_accounts_net

# 启动数据库容器
echo "Starting the MySQL database container..."
docker run -d --name easy_accounts_db \
    --network easy_accounts_net \
    -p 10668:3306 \
    -v $(pwd)/Database/data:/var/lib/mysql \
    -v $(pwd)/Database/init:/docker-entrypoint-initdb.d \
    -e TZ=Asia/Shanghai \
    -e MYSQL_ROOT_PASSWORD=easy_accounts \
    -e MYSQL_DATABASE=yd_jz \
    --restart always \
    registry.cn-beijing.aliyuncs.com/easy_accounts/mysql:8.0.31 \
    --default-authentication-plugin=mysql_native_password \
    --character-set-server=utf8mb4 \
    --collation-server=utf8mb4_general_ci \
    --explicit_defaults_for_timestamp=true \
    --lower_case_table_names=1

# 等待数据库初始化
echo "Waiting for the database to initialize..."
sleep 60

# 启动后端服务器
echo "Starting the server container..."
docker run -d --name easy_accounts_server \
    --network easy_accounts_net \
    -p 10670:8081 \
    -v $(pwd)/Resource/sql:/Ledger/backup \
    -v $(pwd)/Resource/excel/month:/Ledger/excel/month \
    -v $(pwd)/Resource/excel/screen:/Ledger/excel/screen \
    -v $(pwd)/Resource/excel/month:/Ledger/excel/analysis \
    -v $(pwd)/Server/logs:/Ledger/logs \
    -e DB_PASSWORD=easy_accounts \
    -e SQL_BACKUP_TIME="00 00 22 * * ?" \
    --restart always \
    --depends-on easy_accounts_db \
    registry.cn-beijing.aliyuncs.com/easy_accounts/easyaccounts-server:latest

# 启动 Nginx
echo "Starting the Nginx container..."
docker run -d --name easy_accounts_nginx \
    --network easy_accounts_net \
    -p 10669:80 \
    -v $(pwd)/Resource:/usr/share/nginx/html/resources \
    -e API_BASE_URL=http://ip:10670 \
    --restart always \
    --depends-on easy_accounts_server \
    registry.cn-beijing.aliyuncs.com/easy_accounts/easyaccounts-nginx:latest

# 启动 webhook 服务
echo "Starting the webhook container..."
docker run -d --name easy_accounts_webhook \
    --network easy_accounts_net \
    -p 10671:8083 \
    -v $(pwd)/WebHook:/app/ \
    -e LOG_FILE=/app/hook.log \
    -e SEND_SQL_BACKUP=True \
    -e SEND_EXCEL=True \
    -e SMTP_SERVER= \
    -e SMTP_PORT= \
    -e SMTP_MAIL= \
    -e SMTP_PASSWORD= \
    -e SMTP_TO_LIST= \
    --restart always \
    registry.cn-beijing.aliyuncs.com/easy_accounts/easyaccounts-webhook:latest

echo "All containers started successfully."