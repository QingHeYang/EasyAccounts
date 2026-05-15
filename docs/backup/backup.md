# 数据备份与恢复

EasyAccounts 项目提供了定时备份数据库的功能，可以从备份的 SQL 文件中快速恢复数据。

{% hint style="success" %}
**v2.6.1 新增**：支持页面操作恢复数据，无需手动映射 SQL 脚本，详见 [页面恢复数据](#页面恢复数据v261)
{% endhint %}

{% hint style="info" %}
**v2.7.0 变更**：备份时间配置已迁移到前端「系统设置 → 备份」，无需重启容器即可生效
{% endhint %}

## 数据备份(自动)

**v2.7.0 起**：在前端「系统设置 → 备份」中配置备份时间（cron 表达式），默认每天晚上 10 点，修改后立即生效。

**v2.6.x 及更早**：通过 server 容器的 `SQL_BACKUP_TIME` 环境变量配置 cron 表达式，修改后需要重启容器。

```yaml
# v2.6.x 配置方式（v2.7.0+ 已废弃）
environment:
    - SQL_BACKUP_TIME=00 00 22 * * ?          # SQL备份时间 corn表达式,默认每天晚上10点
```

定时备份位置为`/Resource/sql`目录下，可以通过挂载卷修改备份文件目录。

```yaml
volumes:
    - ./Resource/sql:/Ledger/backup            # 数据库备份文件目录
```

备份后的文件如下：

```shell
root@VM-20-8-ubuntu:~/EasyAccounts/Resource# tree
.
├── excel
│   ├── month
│   └── screen
└── sql
    └── yd_jz_20240516_2200.sql                 # 数据库备份文件

5 directories, 1 file
```

## 页面恢复数据（v2.6.1+）

v2.6.1 版本起，支持在页面上直接恢复数据，无需手动操作服务器。

**操作步骤**：

1. 进入 **设置** → **系统信息** → **数据恢复**
2. 选择要恢复的 SQL 备份文件
3. 点击确认，等待恢复完成
4. 恢复完成后系统会自动重载数据

{% hint style="warning" %}
**注意**：恢复操作会覆盖当前数据库，请确保已备份重要数据
{% endhint %}

---

## 数据恢复(手动)

如果你使用的是 v2.6.0 及以下版本，或需要手动恢复数据，请按以下步骤操作：

1. 准备一份数据库备份文件，如 `yd_jz_20250207_2200.sql`
2. 关掉容器：

```shell
docker compose down
```

3. 删除数据库数据文件夹 `/Database/data`，删除掉旧的数据库初始化文件 `/Database/init/*`

```shell
# 删除数据库数据文件夹
rm -rf Database/data
# 删除掉旧的数据库初始化文件
rm -rf Database/init/*
```

4. 拷贝备份文件到数据库初始化文件夹

```shell
cp xxx.sql Database/init/
```

5. 修改 docker-compose.yml，解开 init 目录映射的注释

```yaml
volumes:
  - ./Database/data:/var/lib/mysql
  - ./Database/init:/docker-entrypoint-initdb.d   # 解开此行注释
```

6. 重新启动容器

```shell
docker compose up -d
```

此时，`Database/data` 文件夹应该会重新自动生成，等待数据初始化，进入系统即可

{% hint style="info" %}
**提示**：恢复完成后，建议重新注释掉 init 目录映射，避免下次启动时重复初始化
{% endhint %}

## 忘记密码

参考这里：[重置密码](../faq/faq.md#q2-wang-ji-mi-ma-zen-me-ban)
