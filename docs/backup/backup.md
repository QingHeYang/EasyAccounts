# 数据备份与恢复

EasyAccounts 项目提供了定时备份数据库的功能，可以从备份的sql文件中快速恢复数据。

## 数据备份(自动)

server容器：\
定时备份时间为每天晚上10点，可以通过环境变量`SQL_BACKUP_TIME`修改corn表达式。

```yaml
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

## 数据恢复(手动)

1. 准备一份数据库备份文件，如`yd_jz_20250207_2200.sql`
2. 关掉容器：

```shell
#关掉容器，dockerhub如下
docker-compose down
#阿里云镜像如下
docker-compose -f docker-compose-chinese.yml down
```

3. 删除数据库数据文件夹`/Database/data`，删除掉旧的数据库初始化文件`/Database/init/*`

```shell
#删除数据库数据文件夹
rm -rf Database/data
#删除掉旧的数据库初始化文件
rm -rf Database/init/*
#拷贝备份文件到数据库初始化文件夹
```

4. 拷贝备份文件到数据库初始化文件夹

```shell
cp xxx.sql Database/init/
```

5. 重新启动容器

```shell
#启动容器，dockerhub如下
docker-compose up -d
#阿里云镜像如下
docker-compose -f docker-compose-chinese.yml up -d
```

此时，`Database/data`文件夹应该会重新自动生成\
等待数据初始化，进入系统即可

## 忘记密码

参考这里：[重置密码](../faq/faq.md#q2-wang-ji-mi-ma-zen-me-ban)
