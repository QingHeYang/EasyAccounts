# 飞牛OS部署

> 部署前提示：飞牛OS本质上是一个Debian系统，项目配置与[标准部署文档](/deploy/deploy.md)基本一致

## 部署方式

目前提供两种部署方式：

| 方式 | 说明 | 状态 |
|------|------|------|
| 手动部署 | 使用 Docker Compose 手动部署 | ✅ 可用 |
| FPK 部署 | 使用飞牛应用包一键安装 | 🚧 制作中 |

---

## 方式一：手动部署

### 1. 获取 Compose 文件

从 GitHub 获取 `docker-compose.yml` 文件内容：

[https://github.com/QingHeYang/EasyAccounts/blob/main/docker-compose.yml](https://github.com/QingHeYang/EasyAccounts/blob/main/docker-compose.yml)

### 2. 创建文件夹

在飞牛OS中创建一个用于存放项目数据的文件夹，例如 `EasyAccounts`

### 3. 创建项目

进入 Docker Compose 管理界面，创建新项目：
- 将 `docker-compose.yml` 的内容粘贴到编辑框中
- 勾选「创建项目后立即启动」

### 4. 确认部署

点击「确定」，等待容器拉取和启动完成

### 5. 访问系统

部署完成后，在浏览器输入以下地址访问：

```
http://{NAS地址}:10669
```

---

## 方式二：FPK 部署

> 🚧 FPK 应用包正在制作中，暂时无法提供文件，敬请期待...

