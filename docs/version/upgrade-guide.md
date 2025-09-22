# 升级指南

本指南适用于所有版本的 EasyAccounts 升级操作。

## 通用升级步骤

### 1. 升级前准备

**重要**：升级前请务必备份数据库！

系统每天会自动备份数据库，备份文件保存在 `Resource/sql/` 目录下。
升级前请确认该目录下有最新的备份文件（文件名格式：`yd_jz_YYYYMMDD_HHMM.sql`）。

### 2. 停止服务

根据你的部署方式选择：

**阿里云镜像部署**：
```bash
docker-compose -f docker-compose-chinese.yml down
```

**Docker Hub 部署**：
```bash
docker-compose down
```

### 3. 更新代码和镜像

**拉取最新代码**：
```bash
git pull origin main
```

**更新镜像**：

阿里云镜像：
```bash
chmod +x update-docker-chinese.sh
./update-docker-chinese.sh
```

Docker Hub：
```bash
chmod +x update-docker.sh
./update-docker.sh
```

### 4. 更新配置文件

根据版本更新说明，修改 docker-compose.yml 或 docker-compose-chinese.yml 文件。

常见配置更新：
- 环境变量调整
- 新增服务配置
- 卷映射更新

### 5. 启动服务

**阿里云镜像**：
```bash
docker-compose -f docker-compose-chinese.yml up -d
```

**Docker Hub**：
```bash
docker-compose up -d
```

### 6. 验证升级

```bash
# 查看服务状态
docker ps

# 查看服务日志
docker logs easy_accounts_server -f
```

访问 Web 界面确认功能正常。

## 特定版本升级说明

### 升级到 v2.5.0

- 删除 nginx 的 API_BASE_URL 配置
- 添加图片目录映射
- （可选）配置 AI 服务
- 详见 [v2.5.0 版本说明](v2.5.0.md)

### 升级到 v2.4.0

- 添加登录相关环境变量
- 映射认证文件目录
- 注意前端框架已升级到 Vue 3

## 常见问题

### 1. 升级后无法访问

**检查事项**：
- 端口是否正确映射
- 防火墙是否开放端口
- 容器是否正常启动

### 2. 数据丢失

**解决方案**：
- 从备份恢复数据库
- 检查卷映射是否正确
- 确认数据目录权限

### 3. 配置不生效

**解决方案**：
- 确认修改了正确的 compose 文件
- 重新创建容器：`docker-compose down && docker-compose up -d`
- 清理旧镜像：`docker system prune`

### 4. AI 服务无法启动

**检查事项**：
- API Key 是否正确配置
- 网络是否能访问 LLM 服务
- 查看 AI 服务日志

## 回滚方案

如果升级失败，可以回滚到之前版本：

1. 停止当前服务
2. 切换到之前的代码版本：`git checkout <previous-tag>`
3. 恢复数据库备份
4. 使用之前版本的镜像启动服务

## 获取帮助

- [项目 Issue](https://github.com/QingHeYang/EasyAccounts/issues)
- [项目文档](https://mercys-organization-2.gitbook.io/easyaccounts/)
- [FAQ](../faq/faq.md)