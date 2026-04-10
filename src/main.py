import random
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# 인증코드 임시 저장 { email: { code, expires_at } }
verify_store: dict = {}

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    code: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/auth/send-code")
def send_code(req: EmailRequest):
    code = str(random.randint(100000, 999999))
    expires_at = datetime.now() + timedelta(minutes=5)
    verify_store[req.email] = {"code": code, "expires_at": expires_at}
    try:
        msg = MIMEText(f"Persona Frame 인증번호: {code}\n\n5분 이내에 입력해주세요.")
        msg["Subject"] = "[Persona Frame] 이메일 인증번호"
        msg["From"] = GMAIL_USER
        msg["To"] = req.email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.sendmail(GMAIL_USER, req.email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이메일 전송 실패: {str(e)}")
    return {"message": "인증번호가 발송되었습니다."}

@app.post("/auth/verify-code")
def verify_code(req: VerifyRequest):
    entry = verify_store.get(req.email)
    if not entry:
        raise HTTPException(status_code=400, detail="인증번호를 먼저 요청해주세요.")
    if datetime.now() > entry["expires_at"]:
        del verify_store[req.email]
        raise HTTPException(status_code=400, detail="인증번호가 만료되었습니다.")
    if entry["code"] != req.code:
        raise HTTPException(status_code=400, detail="인증번호가 올바르지 않습니다.")
    del verify_store[req.email]
    return {"message": "인증 완료"}
