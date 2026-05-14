import random
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from ..core.database import get_db
from ..core.security import create_access_token
from ..schemas.auth import EmailRequest, VerifyRequest, RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")


@router.post("/send-code")
def send_code(req: EmailRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (req.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        code = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=5)

        cursor.execute(
            "INSERT INTO email_verifications (email, code, expires_at) VALUES (%s, %s, %s)",
            (req.email, code, expires_at),
        )
        db.commit()

        msg = MIMEText(f"Persona Frame 인증번호: {code}\n\n5분 이내에 입력해주세요.")
        msg["Subject"] = "[Persona Frame] 이메일 인증번호"
        msg["From"] = GMAIL_USER
        msg["To"] = req.email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.sendmail(GMAIL_USER, req.email, msg.as_string())

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "인증번호가 발송되었습니다."}


@router.post("/verify-code")
def verify_code(req: VerifyRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM email_verifications
            WHERE email = %s AND code = %s AND is_used = FALSE
            ORDER BY created_at DESC LIMIT 1
            """,
            (req.email, req.code),
        )
        entry = cursor.fetchone()

        if not entry:
            raise HTTPException(status_code=400, detail="인증번호가 올바르지 않습니다.")

        if datetime.now() > entry["expires_at"]:
            raise HTTPException(status_code=400, detail="인증번호가 만료되었습니다.")

        cursor.execute(
            "UPDATE email_verifications SET is_used = TRUE WHERE id = %s",
            (entry["id"],),
        )
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    return {"message": "인증 완료"}


@router.post("/register")
def register(req: RegisterRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (req.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        cursor.execute(
            """
            SELECT * FROM email_verifications
            WHERE email = %s AND is_used = TRUE
            ORDER BY created_at DESC LIMIT 1
            """,
            (req.email,),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="이메일 인증이 필요합니다.")

        cursor.execute(
            "INSERT INTO users (email, password, name, location) VALUES (%s, %s, %s, %s) RETURNING id",
            (req.email, req.password, req.nickname or "", ""),
        )
        user_id = str(cursor.fetchone()["id"])
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    token = create_access_token(user_id)
    return {"message": "회원가입이 완료되었습니다.", "access_token": token}


@router.post("/login")
def login(req: LoginRequest):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (req.email,))
        user = cursor.fetchone()

        if not user or user["password"] != req.password:
            raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        db.close()

    token = create_access_token(str(user["id"]))
    return {"message": "로그인 성공", "email": req.email, "nickname": user["name"], "access_token": token}
