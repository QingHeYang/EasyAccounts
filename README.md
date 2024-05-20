# EasyAccounts
**中文记账软件**  
EasyAccounts是一款中文记账软件，主要的作用是简易记账  
特色功能有，生成Excel账单，定时备份数据库、账单数据  
|  [项目部署](./README-Deploy.md) ｜ 功能介绍 |    

## 功能  
项目主体功能是基于账户的记账，所有的金额都是基于账户来进行的。  
### 可以定义的操作有
1. 账户：有金额、名称等选项。
2. 操作：收入、支出、借入、借出、内部转账等选项，此项目我已经再初始化数据库中添加了常用的几项，足够覆盖生活99%以上的场景，不建议修改。  
3. 类型：有一二级类型，例如用车支出，下属可以选择：加油、保险，具体选项参考自己日常生活，需要注意的是，分类与操作没有关联，你可以叫做 “我的收入”,但是你记账的时候可以选择“支出”操作，**分类仅用于快捷记录使用**。  

### 记账功能  
选择账户->选择操作->选择记账类型->输入金额->保存。  
一条账目就记录完毕，所在金额会在选择的账户中增加或减少。  

### 报表功能  
一共可以生成三种文档：
- 月度账单：生成一个月的账单。
    - 位置：主页流水选项卡里，如果你有流水记录，点击生成报表，没有记录的话就没有这个按钮。
    - 可以生成一个月的流水账单，有一点一定要记住，生成账单的时间点，再excel里面是会有你所有的账户金额的，所以如果你再5月记账，生成4月的账单，那么4月的账单里面是有5月的账户金额的，所以生成账单的时候一定要注意时间点。**请在记录当月的流水之前，生成上个月的账单。**
- 筛选账单：生成筛选的账单。
    - 位置：主页点击总览，然后点击筛选按钮，选择筛选条件，然后点击生成报表。
    - 生成报表前，记得点筛选验证数据，如果没有筛选结果数据，是不会生成报表的，接口会报错，哈哈哈，这是一个小bug，我懒得改了。
- 分析报表：生成分析同环比报表。
    - 位置：主页点击分析选项卡，然后选择周期，点击生成报表。
    - 生成完的同比环比数据会汇总到一个Excel表格中，可以查看同比环比数据。

### 筛选功能  
基本所有的操作包括类型，都可以算作筛选的选项，得到结果后可以手动生成xls。  

### 备份功能  
启动项目的时候可以设置SQL备份日期规则，使用cron规则，详情见docker-compose.yml文件中的环境变量。  
备份的文件会存放在Resource/sql目录下，文件名为日期.sql。  
Excel生成后，会自动备份到Resource/excel目录下，对应上面三个账单的文件夹。  

### WebHook功能  
WebHook是我在开源之前临时突击的功能。  
主要是不知道使用者们有什么备份习惯。  
```Python
@app.post("/webhook")
async def handle_webhook(file: UploadFile = File(...), file_name: str = Form(...), file_type: str = Form(...)):
    logger.info(f"Received request with file_name: {file_name} and file_type: {file_type}")
    try:
        file_content = await file.read()
        if file_type == "sql":
            result = await handleMySqlBackUp(file_content, file_name)
        elif file_type == "analysis_excel":
            result = await handleMonthExcelBackUp(file_content, file_name)
        elif file_type == "month_excel":
            result = await handleMonthExcelBackUp(file_content, file_name)
        elif file_type == "screen_excel":
            result = await handleScreenExcelBackUp(file_content, file_name)
        
        await send_webhook(file_content, file_name, file_type)
        logger.info(result)
        
        return {"status": "ok", "result": result}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"status": "error", "message": str(e)}

# 处理备份数据库的逻辑
async def handleMySqlBackUp(file_content: bytes, file_name: str):
    logger.info(f"Handling MySQL backup with file_name: {file_name}")
    return f"Handled MySQL backup for file_name: {file_name}"

# 处理备份月度账单的逻辑
async def handleMonthExcelBackUp(file_content: bytes, file_name: str):
    logger.info(f"Handling monthly Excel backup with file_name: {file_name}")
    return f"Handled monthly Excel backup for file_name: {file_name}"

# 处理备份筛选账单的逻辑
async def handleScreenExcelBackUp(file_content: bytes, file_name: str):
    logger.info(f"Handling screen Excel backup with file_name: {file_name}")
    return f"Handled screen Excel backup for file_name: {file_name}"

# 工具方法: 将文件保存到本地
async def save_file_locally(file: UploadFile, file_path: str):
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        logger.info(f"File {file.filename} saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save file {file.filename} to {file_path}: {str(e)}")



async def send_webhook(file: bytes, file_name: str, file_type: str):
    try:
        files = {"file": (file_name, file)}
        data = {"file_type": file_type}
        response = requests.post(JAVA_ENDPOINT, files=files, data=data)
        response.raise_for_status()
        logger.info(f"Webhook sent successfully. Response: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send webhook: {str(e)}")
```

这段代码是一个收到文件后的处理逻辑，主要是备份数据库和Excel文件。  
你可以再python中使用requests库，发送文件到这个接口，然后这个接口会处理你发送的文件。  
我自己用的阿里云OSS备份，用了阿里云的Email服务，但是注册阿里云很多人不会，所以我干脆就开放了WebHook功能。

## 注意  
强烈建议尝试实现一下WebHook功能，这样你的数据就不会丢失了。  
如果你不会写代码也无所谓，但是一定要记得定时备份数据库文件、Excel文件。  
如果你不会写代码，我也可以帮你写。  

还有就是要注意，项目是没有使用任何Auth鉴权的，所以一定要注意项目的安全性。
我是不推荐暴露端口到公网的，如果你要暴露端口到公网，一定要注意安全性。  

基于上述原则，后需我也不会增加登录功能，因为没有任何系统是安全的，何况是个人开发者的项目。  

## 部署
项目部署，和使用上面，我到时候会录一个视频，放到B站上，到时候我会更新这个文档。