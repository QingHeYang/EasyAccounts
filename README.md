# EasyAccounts 项目说明  
## 前言  
该项目是一款开源的记账软件，采用复式记账方法。  
做该项目的起因是当初使用很多国内的互联网记账软件，结果因为经营不善，亦或者政策缘故，导致软件停止维护，最终账单丢失。  
本意是给家人使用，但由于我在各个论坛逛的时候，发现还是有部分人有需求的，就花了段时间开源该项目。  
## 功能  
项目主体功能是基于账户的记账，所有的金额都是基于账户来进行的。  
### 可以定义的操作有
1. 账户：有金额、名称等选项。
2. 操作：收入、支出、借入、借出、内部转账等选项。  
3. 类型：有一二级类型，例如用车支出，下属可以选择：加油、保险，具体选项参考自己日常生活。  

### 记账功能  
选择账户->选择操作->选择记账类型->输入金额->保存。  
一条账目就记录完毕，所在金额会在选择的账户中增加或减少。  
### 报表功能  
用户可以在启动项目的时候设置每月生成账单日期，使用cron规则。  
会按照用户的规则生成xls的每月报表。  
### 筛选功能  
基本所有的操作包括类型，都可以算作筛选的选项，得到结果后可以手动生成xls。  
### 备份功能  
启动项目的时候可以设置备份日期规则，使用cron规则。  
在在定时日期备份出一份sql文件，方便用户存储数据。  
### 附加功能（可选）  
1. 云存储功能，用户可以设置阿里云oss的key,设置完毕后，重启项目，每月定时备份会上传到oss对应的路径中。  
2. Email功能，用户可以配置发送邮件规则，生成报表后，会将报表发送到对应的邮箱中。  

## 项目架构  
前端：VUE  
后端：Python+FastApi  
数据库：MariaDB  

## 部署方法  
复制docker-compose.yaml 
