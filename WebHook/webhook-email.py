import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

# 读取环境变量
SMTP_SERVER = os.getenv('SMTP_SERVER', '')
SMTP_PORT = os.getenv('SMTP_PORT', '')
SMTP_FROM = os.getenv('SMTP_MAIL', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_TO_LIST = os.getenv('SMTP_TO_LIST', '')
SEND_SQL_BACKUP = os.getenv('SEND_SQL_BACKUP', 'True')
SEND_EXCEL = os.getenv('SEND_EXCEL', 'True')

# 配置日志
logging.basicConfig(filename='hook.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(file: UploadFile = File(...), file_name: str = Form(...), file_type: str = Form(...)):
    if(file_type == "sql_backup" and SEND_SQL_BACKUP == 'False'):
        return {"status": "ok", "result": "SQL 备份邮件发送功能已关闭"}
    if(file_type == "month_excel" and SEND_EXCEL == 'False'):
        return {"status": "ok", "result": "月度 Excel 发送功能已关闭"}
    if(file_type == "screen_excel" and SEND_EXCEL == 'False'):
        return {"status": "ok", "result": "筛选账单 Excel 发送功能已关闭"}
    if(file_type == "analysis_excel" and SEND_EXCEL == 'False'):
        return {"status": "ok", "result": "财务分析 Excel 发送功能已关闭"}
    if not await check_smtp_info():
        return {"status": "error", "message": "SMTP 信息不完整，请设置环境变量"}
    else:
        logger.info(f"收到文件: {file_name} & 文件类型为: {file_type}")
        try:
            file_content = await file.read()
            result = await send_email_with_attachment(file_content,file_name, file_type)
            logger.info(result)
            return {"status": "ok", "result": result}
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            return {"status": "ok", "result": "请检查是否收到邮件"}



async def send_email_with_attachment(file_content: bytes, file_name: str, file_type: str):
    logger.info(f"发送邮件名称为： {file_name} 收件人列表为： {SMTP_TO_LIST}")
    msg = MIMEMultipart()

    if file_type == "sql" and SEND_SQL_BACKUP=='True':
        msg['Subject'] = 'SQL 备份日志，备份文件名：' + file_name
        body = MIMEText(f'账单SQL备份（{file_name}）。记得保存好，以防不时之需', 'plain')
    elif file_type == "month_excel" and SEND_EXCEL=='True':
        msg['Subject'] = file_name+ ' 月度 Excel 已生成，请查收'
        body = MIMEText(f'月度账单 Excel({file_name}) 已生成，请查收', 'plain')
    elif file_type == "analysis_excel" and SEND_EXCEL=='True':
        msg['Subject'] = file_name+ ' 财务分析 Excel 已生成，请查收'
        body = MIMEText(f'财务分析 Excel({file_name}) 已生成，请查收', 'plain')
    elif file_type == "screen_excel" and SEND_EXCEL=='True':
        msg['Subject'] = file_name+ ' 筛选账单 Excel 已生成，请查收'
        body = MIMEText(f'筛选账单 Excel({file_name}) 已生成，请查收', 'plain')

    if body is None:
        logger.info("用户选择不发送邮件")
        return "用户选择不发送邮件"
    else:
        recipient_list = [email.strip() for email in SMTP_TO_LIST.split(",")]
        # 设置发件人、收件人
        msg['From'] = SMTP_FROM
        msg['To'] = ", ".join(recipient_list)
        msg.attach(body)
        # 邮件附件处理
        file_name = file_name.replace(' ', '')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        part.add_header('Content-Type', 'application/octet-stream', name=file_name)
        msg.attach(part)

        # 连接到 SMTP 服务器并发送邮件
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # 与服务器打招呼
            server.starttls()  # 启用TLS
            server.ehlo()  # 重新与服务器打招呼
            server.login(SMTP_FROM, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, recipient_list, msg.as_string())
        logger.info(f"文件 {file_name} 已发送到 {recipient_list}")
        return f"文件 {file_name} 已发送到 {recipient_list}，发送结果：OK"


async def check_smtp_info():
    logger.info("检查 SMTP 信息,打印环境变量")
    logger.info(f"SMTP_SERVER: {SMTP_SERVER}\nSMTP_PORT: {SMTP_PORT}\nSMTP_FROM: {SMTP_FROM}\nSMTP_PASSWORD: {len(SMTP_PASSWORD)}位\nSMTP_TO: {SMTP_TO_LIST}\n SEND_SQL_BACKUP: {SEND_SQL_BACKUP}\nSEND_EXCEL: {SEND_EXCEL}")
    if not SMTP_SERVER or not SMTP_PORT or not SMTP_FROM or not SMTP_PASSWORD or not SMTP_TO_LIST:
        logger.error("SMTP 信息缺失，请设置环境变量")
        return False
    return True