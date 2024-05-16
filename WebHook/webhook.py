from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
import logging
import requests

# 你的 Java Spring Boot 接口地址
JAVA_ENDPOINT = "http://192.168.50.226:10672/EasyAccounts/webhook"

app = FastAPI()

# 配置日志
logging.basicConfig(filename='hook.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定义数据模型
class WebhookData(BaseModel):
    file_name: str
    file_type: str

@app.post("/webhook")
async def handle_webhook(file: UploadFile = File(...), file_name: str = Form(...), file_type: str = Form(...)):
    logger.info(f"Received request with file_name: {file_name} and file_type: {file_type}")
    try:
        file_content = await file.read()
        if file_type == "sql":
            result = await handleMySqlBackUp(file_content, file_name)
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